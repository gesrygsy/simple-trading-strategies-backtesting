from logging import raiseExceptions
from os import path, makedirs, listdir
import pandas as pd
import numpy as np

from loader.load_data import load_data
from loader.calculators import calc_margin, calc_profit, calc_profit_cross, calc_drawdown
from loader.instruments import inst_prop

def backtest_conclude(data, param):
    data['Entry_Price'], data['Margin'], data['Loss'], data['Profit'], data['Drawdown'] = np.nan, np.nan, np.nan, np.nan, np.nan
    f_symbol = str(param['symbol'][:3])
    t_symbol = str(param['symbol'][-3:])
    pol = data['PoL'].value_counts()
    data_source = str(param['data_source'])
    try:
        winrate = round(pol['True'] / (pol['False'] + pol['True']) * 100, 2)
    except:
        raiseExceptions
        winrate = 0

    
    if param['batch_run'][0] is False:
        leverage = 500
        path_ = path.abspath("") + '/Data/' + data_source + '/Backtest Results/'
        data_dir = path_ + param['symbol'] + '/'
        # data.set_index('Datetime', inplace=True)

        data.loc[((data['Num_Trade']%1) == 0.5) & (data['Trade'] != 0), 'Entry_Price'] = data['Open']
        data.loc[((data['Num_Trade']%1) == 0.5) & (data['Trade'] == 0), 'Entry_Price'] = data['Entry_Price'].fillna(method='ffill')

        data['Margin'] = calc_margin(inst_prop[param['symbol']]['type'], leverage, param['symbol'], data['Entry_Price'], abs(data['aPosition']))
        data['Loss'] = calc_profit(inst_prop[param['symbol']]['type'], param['symbol'], data[f"D_CLr{param['cl_ratio']}"]/param['trading_size'], data['Entry_Price'], abs(data['aPosition']))
        try:
            data['Profit'] = calc_profit(inst_prop[param['symbol']]['type'], param['symbol'], data[f"D_TPr{param['tp_ratio']}"]/param['trading_size'], data['Entry_Price'], abs(data['aPosition']))
        except:
            pass

        if f_symbol == 'USD':
            data[f"PnL({f_symbol})"], data[f"Total_PnL({f_symbol})"] = np.nan, np.nan
            data.loc[(data['Num_Trade'] >= 1) & (data['Trade'] != 0), f"PnL({f_symbol})"] = data['Trade_PoL'] * 100000 / data['Entry_Price'].shift(1)
            data[f"Total_PnL({f_symbol})"] = data[f"PnL({f_symbol})"].cumsum()
            data.loc[(data['Trade'] == 0) | (data['Trade'] == data['Position']), f'Total_PnL({f_symbol})'] = data[f"Total_PnL({f_symbol})"].fillna(method='ffill')
        elif t_symbol == 'USD':
            data[f"PnL({t_symbol})"], data[f"Total_PnL({t_symbol})"] = np.nan, np.nan
            data.loc[(data['Num_Trade'] >= 1) & (data['Trade'] != 0), f"PnL({t_symbol})"] = data['Trade_PoL'] * 100000
            data[f"Total_PnL({t_symbol})"] = data[f"PnL({t_symbol})"].cumsum()
            data.loc[(data['Trade'] == 0) | (data['Trade'] == data['Position']), f'Total_PnL({t_symbol})'] = data[f"Total_PnL({t_symbol})"].fillna(method='ffill')
        else:
            data[f"PnL({t_symbol})"], data[f"Total_PnL({t_symbol})"] = np.nan, np.nan
            data.loc[(data['Num_Trade'] >= 1) & (data['Trade'] != 0), f"PnL({t_symbol})"] = data['Trade_PoL'] * 100000
            data[f"Total_PnL({t_symbol})"] = data[f"PnL({t_symbol})"].cumsum()
            data.loc[(data['Trade'] == 0) | (data['Trade'] == data['Position']), f'Total_PnL({t_symbol})'] = data[f"Total_PnL({t_symbol})"].fillna(method='ffill')

            try:
                path_ = path.abspath("") + '/Data/' + data_source + '/' + param['to_date'] + '/'
            except:
                path_ = path.abspath("") + '/Data/' + data_source + '/'
            symbol_list = listdir(path_)
            param_fsymbol = {}
            param_usd = {}
            param_fsymbol['symbol'] = [_ for _ in symbol_list if (_ == f"USD{f_symbol}") or (_ == f"{f_symbol}USD")][0]
            param_fsymbol['timeframe'] = param['timeframe']
            param_fsymbol['trading_mode'] = param['trading_mode']
            param_usd['symbol'] = [_ for _ in symbol_list if (_ == f"USD{t_symbol}") or (_ == f"{t_symbol}USD")][0]
            param_usd['timeframe'] = param['timeframe']
            param_usd['trading_mode'] = param['trading_mode']
            param_fsymbol['data_source'] = param['data_source']
            param_usd['data_source'] = param['data_source']
            try:
                param_fsymbol['to_date'] = param['to_date']
                param_usd['to_date'] = param['to_date']
            except:
                pass
            data_fsymbol = load_data(param_fsymbol)
            try:
                data_fsymbol.drop(columns=['Close', 'High', 'Low', 'Tick_Volume'], inplace=True) 
            except:
                data_fsymbol.drop(columns=['Close', 'High', 'Low'], inplace=True)
            data_fsymbol.rename(columns={'Open': f"Open({param_fsymbol['symbol']})"}, inplace=True)
            data = pd.merge(data, data_fsymbol, how='inner', left_index=True, right_index=True)
            
            data_usd = load_data(param_usd)
            try:
                data_usd.drop(columns=['Close', 'High', 'Low', 'Tick_Volume'], inplace=True)
            except:
                data_usd.drop(columns=['Close', 'High', 'Low'], inplace=True)
            data_usd.rename(columns={'Open': f"Open({param_usd['symbol']})"}, inplace=True)
            data = pd.merge(data, data_usd, how='inner', left_index=True, right_index=True)
            data[f"Open({param_usd['symbol']})"].fillna(method='bfill', inplace=True)
            data[f"Open({param_usd['symbol']})"].fillna(method='ffill', inplace=True)

            data[f"Entry_Price({param_usd['symbol']})"], data[f"Entry_Price({param_fsymbol['symbol']})"], data["PnL(USD)"], data["Total_PnL(USD)"] = np.nan, np.nan, np.nan, np.nan
            data.loc[((data['Num_Trade']%1) == 0.5) & (data['Trade'] != 0), f"Entry_Price({param_fsymbol['symbol']})"] = data[f"Open({param_fsymbol['symbol']})"]
            data.loc[((data['Num_Trade']%1) == 0.5) & (data['Trade'] == 0), f"Entry_Price({param_fsymbol['symbol']})"] = data[f"Entry_Price({param_fsymbol['symbol']})"].fillna(method='ffill')
            data.loc[((data['Num_Trade']%1) == 0.5) & (data['Trade'] != 0), f"Entry_Price({param_usd['symbol']})"] = data[f"Open({param_usd['symbol']})"]
            data.loc[((data['Num_Trade']%1) == 0.5) & (data['Trade'] == 0), f"Entry_Price({param_usd['symbol']})"] = data[f"Entry_Price({param_usd['symbol']})"].fillna(method='ffill')

            data['Margin'] = calc_margin(inst_prop[param_fsymbol['symbol']]['type'], leverage, param_fsymbol['symbol'], data[f"Entry_Price({param_fsymbol['symbol']})"], abs(data['aPosition']))
            data['Loss'] = calc_profit_cross(inst_prop[param_usd['symbol']]['type'], param_usd['symbol'], data[f"D_CLr{param['cl_ratio']}"]/param['trading_size'], data[f"Entry_Price({param_usd['symbol']})"], abs(data['aPosition']))
            try:
                data['Profit'] = calc_profit(inst_prop[param_usd['symbol']]['type'], param_usd['symbol'], data[f"D_TPr{param['tp_ratio']}"]/param['trading_size'], data[f"Entry_Price({param_usd['symbol']})"], abs(data['aPosition']))
            except:
                pass

            if str(param_usd['symbol'][:3]) == 'USD':
                data.loc[(data['Num_Trade'] >= 1) & (data['Trade'] != 0), "PnL(USD)"] = data[f"PnL({t_symbol})"] / data[f"Entry_Price({param_usd['symbol']})"].shift(1)
                data["Total_PnL(USD)"] = data["PnL(USD)"].cumsum()
                data.loc[(data['Trade'] == 0) | (data['Trade'] == data['Position']), f'Total_PnL(USD)'] = data[f"Total_PnL(USD)"].fillna(method='ffill')
            else:
                data.loc[(data['Num_Trade'] >= 1) & (data['Trade'] != 0), "PnL(USD)"] = data[f"PnL({t_symbol})"] * data[f"Entry_Price({param_usd['symbol']})"].shift(1)
                data["Total_PnL(USD)"] = data["PnL(USD)"].cumsum()
                data.loc[(data['Trade'] == 0) | (data['Trade'] == data['Position']), f'Total_PnL(USD)'] = data[f"Total_PnL(USD)"].fillna(method='ffill')
                
        if not any(_ == 'composite' for _ in param.keys()):
            data.loc[data['Loss'] < 0, 'Drawdown'] = calc_drawdown(data['Loss'], possible_losses=1.2)

            columns = []
            for col in data.columns:
                columns.append(col)
            data = pd.DataFrame(data=data, columns=columns)

            if param['trailing_stop'] is True:
                extend_file_name = '_TS'
            else:
                extend_file_name = ''

            if param['cl_stop'] is True:
                extend_file_name = extend_file_name + '_CLs'
            if param['tp_stop'] is True:
                extend_file_name = extend_file_name + '_TPs'

            if param['strategy'] == 'RSI':
                file_name = f"check {param['symbol']}(RSI{param['period']}_MA{param['period_ma']}_R{param['rsi_range']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'MFI':
                file_name = f"check {param['symbol']}(MFI{param['period']}_MA{param['period_ma']}_R{param['mfi_range']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'BBands':
                file_name = f"check {param['symbol']}(BBands{param['period']}_MA{param['period_ma']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'Stoch':
                file_name = f"check {param['symbol']}(Stoch_fk{param['fastk']}_sk{param['slowk']}_sd{param['slowd']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'Stochf':
                file_name = f"check {param['symbol']}(Stochf_fk{param['fastk']}_fd{param['fastd']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'StochRSI':
                file_name = f"check {param['symbol']}(StochRSI{param['period']}_fk{param['fastk']}_fd{param['fastd']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'MACD':
                file_name = f"check {param['symbol']}(MACD_f{param['fastperiod']}_s{param['slowperiod']}_sig{param['signalperiod']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'ROC':
                file_name = f"check {param['symbol']}(ROC{param['period']}_MA{param['period_ma']}_TH{param['threshold']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'ADX':
                file_name = f"check {param['symbol']}(ADX{param['period']}_MA{param['period_ma']}_RO{param['period_ro']}_TH{param['threshold']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'MOM':
                file_name = f"check {param['symbol']}(MOM{param['period_mom']}_R{param['period_range']}_MA{param['period_ma']}_TH{param['threshold']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'KAMA':
                try:
                    file_name = f"check {param['symbol']}(KAMA{param['period']}_MA{param['period_ma']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
                except:
                    file_name = f"check {param['symbol']}(KAMA{param['period']}_MA{param['period_ma']}_CLr{param['cl_ratio']}_CrossTP_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'Hilbert':
                file_name = f"check {param['symbol']}(Hilbert_MA{param['period_ma']}_CLr{param['cl_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'PPO':
                file_name = f"check {param['symbol']}(PPO_f{param['fastperiod']}_s{param['slowperiod']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"
            elif param['strategy'] == 'Chaikin_AD':
                file_name = f"check {param['symbol']}(ChaikinAD_f{param['fastperiod']}_s{param['slowperiod']}_MA{param['period_ma']}_CLr{param['cl_ratio']}_TPr{param['tp_ratio']}_De{param['decay']}_Size{param['trading_size']}{extend_file_name} {param['timeframe']}).csv"

            try:
                data.to_csv(data_dir + file_name, float_format='%.4f', index=True)
            except Exception as e:
                print('Error: ', e)
                print('Creating folder/file...')
                makedirs(data_dir, exist_ok=True)
                data.to_csv(data_dir + file_name, float_format='%.4f', index=True)
            else:
                print(f"Updated {file_name}.")
            
            last_num_trade = list(data['Num_Trade'])[-1]
            last_pos_period = list(data['Pos_period'])[-1]
            last_cum_pnl = list(data['Cum_PnL'])[-1] / param['pip']
            print('WinRate: ', str(winrate) + '%')
            print('Num_Trade: ', str(list(data['Num_Trade'])[-1]))
            print('Total_PnL: ', format(last_cum_pnl, '.4f'))
            print('PnL_Trade: ', str(format(last_num_trade and ((last_cum_pnl / last_num_trade) or 0), '.4f')))
            print('Hold_Period: ', str(list(data['Pos_period'])[-1]))
            print('PnL_Period: ', str(format(last_pos_period and ((last_cum_pnl / last_pos_period) or 0), '.4f')))
        
        return data, data_dir
    
    return winrate