import talib, time, sys
import numpy as np
import concurrent.futures
from itertools import product, groupby

from loader.load_data import load_data
from loader.instruments import inst_prop
from loader.timestr import timestr
from loader.calculators import *
from backtesting.calc_cumpnl import calc_cumpnl
from backtesting.conclude import backtest_conclude
from backtesting.batch_run_summary import batch_run_summary
from backtesting.show_plt import show_plt

def rsi_main(param):
    data = load_data(param)
    param['pip'] = inst_prop[param['symbol']]['pip']

    data['Price_Diff'] = data['Open'].diff().fillna(0)

    data[f"RSI{param['period']}"] = talib.RSI(data['Close'], param['period'])
    data[f"MA{param['period_ma']}"] = round(talib.MA(data['Close'], param['period_ma']), 5)

    data[f"ATR{param['atr']}"] = round(talib.ATR(data['High'], data['Low'], data['Close'], timeperiod=param['atr']), 5).shift(1)
    data[f"CLr{param['cl_ratio']}"] = round(data[f"ATR{param['atr']}"] * -param['cl_ratio'], 4)
    data[f"TPr{param['tp_ratio']}"] = round(data[f"ATR{param['atr']}"] * param['tp_ratio'], 4)

    data['Trend'], data['Signal'], data['Signal_T'], data['Position'], data['aPosition'] = 0, 0, 0, 0, 0

    data.loc[(data['Close'].shift(1) / data[f"MA{param['period_ma']}"].shift(1)) > 1.01, 'Trend'] = 1
    data.loc[(data['Close'].shift(1) / data[f"MA{param['period_ma']}"].shift(1)) < 0.99, 'Trend'] = -1

    data.loc[(data['Trend'] == 0) & (data[f"RSI{param['period']}"].shift(1) > (50 + param['rsi_range'])), 'Signal'] = -1
    data.loc[(data['Trend'] == 0) & (data[f"RSI{param['period']}"].shift(1) < (50 - param['rsi_range'])), 'Signal'] = 1

    data['Signal_s'] = data['Signal'].shift(1)
    data.loc[(data['Signal_s'] == 1) & (data['Signal'] == 0), 'Signal_T'] = 1
    data.loc[(data['Signal_s'] == -1) & (data['Signal'] == 0), 'Signal_T'] = -1
    data = data.drop('Signal_s', axis=1)

    data['PnL'], data['Cum_PnL'], data['Trade_PoL'], data['Period'] = 0, 0, 0, 0
    data[f"D_CLr{param['cl_ratio']}"], data[f"D_TPr{param['tp_ratio']}"] = 0, 0
        
    position, aposition, trade_pol, period, pnl, d_clr, d_tpr, cum_pnl = [0], [0], [0], [0], [0], [0], [0], [0]

    for _, r in data.iterrows():
        output = calc_cumpnl(r, param, position[-1], aposition[-1], trade_pol[-1], period[-1], d_clr[-1], d_tpr[-1], cum_pnl[-1])
        position.append(output[0])
        aposition.append(output[1])
        trade_pol.append(output[2])
        period.append(output[3])
        pnl.append(output[4])
        d_clr.append(output[5])
        d_tpr.append(output[6])
        cum_pnl.append(output[7])

    data['Position'] = position[1:]
    data['aPosition'] = aposition[1:]
    data['Trade_PoL'] = trade_pol[1:]
    data['Period'] = period[1:]
    data['PnL'] = pnl[1:]
    data[f"D_CLr{param['cl_ratio']}"] = d_clr[1:]
    data[f"D_TPr{param['tp_ratio']}"] = d_tpr[1:]
    data['Cum_PnL'] = cum_pnl[1:]

    if not param['trading_mode']:
        data['Trade'] = data['Position'].diff()
        data['Num_Trade'] = abs(data['Trade']).cumsum() / 2
        data.loc[abs(data['Num_Trade'] <= 0), 'Num_Trade'] = 0.001

        data['Entry'], data['PoL'], data['Pos_period'] = np.nan, np.nan, 0

        data.loc[(data['Trade'] != 0) & (data['aPosition'] != 0), 'Entry'] = data['Cum_PnL'].shift(1)
        data.loc[(data['aPosition'] != 0), 'Entry'] = data['Entry'].fillna(method='ffill')
        data.loc[(data['Trade'] != 0) & (data['Num_Trade']%1 != 0.5) & (data['Cum_PnL'] - data['Entry'].shift(1) > 0), 'PoL'] = 'True'
        data.loc[(data['Trade'] != 0) & (data['Num_Trade']%1 != 0.5) & (data['Cum_PnL'] - data['Entry'].shift(1) < 0), 'PoL'] = 'False'
        data.loc[data['Trade_PoL'] != 0, 'Pos_period'] = 1
        data['Pos_period'] = data['Pos_period'].cumsum()

        if param['batch_run'] == True:
            param['batch_run'] = [True]
        if param['batch_run'] == False:
            param['batch_run'] = [False]

        if param['batch_run'][0]:
            sym = param['symbol']
            strategy = 'RSI'
            if param['trailing_stop']:
                extend_com_param = '_TS'
            else:
                extend_com_param = ''
            com_param = f"RSI{param['period']}_MA{param['period_ma']}_R{param['rsi_range']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_com_param}"
            winrate = backtest_conclude(data, param)
            num_trade = list(data['Num_Trade'])[-1]
            total_pnl = list(data['Cum_PnL'])[-1] / param['pip']
            # Avoid ZeroDivisionError (a/b)     # result = b and a/b or 0 
            pnl_trade = num_trade and (total_pnl / num_trade) or 0
            hold_period = list(data['Pos_period'])[-1]
            pnl_period = hold_period and (total_pnl / hold_period) or 0

            return sym, strategy, com_param, winrate, num_trade, total_pnl, pnl_trade, hold_period, pnl_period
        else:
            data, data_dir = backtest_conclude(data, param)
            return data, data_dir
    else:
        return data
    
def rsi_backtest(kwargs):
    start = time.perf_counter()
    param = {}

    for key, value in kwargs.items():
        param[key] = value
    
    param['batch_run'] = [any(type(_) is list for _ in param.values())]

    if param['batch_run'][0]:
        param['trading_mode'] = [False]
        prods = [dict(zip(param, v)) for v in product(*param.values())]
        print(len(prods))
        all_results = []
        results = {}
        task = 0
        
        def task_status(task, t1):
            t2 = time.perf_counter()
            printing = f'Running task {task}/{len(prods)} ({round(task/len(prods)*100,1)}% Completed) in {str(round((t2-t1)/task,2))} sec(s)/task.'
            sys.stdout.write('\r' + printing)
            sys.stdout.flush()

        with concurrent.futures.ProcessPoolExecutor() as executor:
            t1 = time.perf_counter()
            batch_results = [executor.submit(rsi_main, prod) for prod in prods]
            
            for f in concurrent.futures.as_completed(batch_results):
                all_results.append(f.result())
                task += 1
                task_status(task, t1)
            sys.stdout.write('\n')

        all_results.sort()
        group_obj = groupby(all_results, key=lambda x: x[0])
        
        for key, value in group_obj:
            results[key] = list(value)
            
        data_source = str(param['data_source'][0])
        batch_run_summary(results, int(len(prods)/len(param['symbol'])), data_source, param['timeframe'][0])
        
        param['show_plt'] = False
    else:
        if not param['trading_mode']:
            data, data_dir = rsi_main(param)
        else:
            data = rsi_main(param)
            param['show_plt'] = False

    end = time.perf_counter()

    print('Finished calculation in ' + timestr(round(end - start, 1)))

    if param['show_plt']:
        show_plt(data=data, data_dir=data_dir, down_sampling=True, **param)
    
    if any(_ == 'composite' for _ in param.keys()):
        return data