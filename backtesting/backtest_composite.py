import matplotlib.pyplot as plt
import numpy as np
from os import path, makedirs

from backtesting.backtest_rsi import rsi_backtest
from backtesting.backtest_adx import adx_backtest
from backtesting.backtest_kama import kama_backtest
from loader.load_data import load_data
from loader.calculators import calc_drawdown, calc_balance_drawdown
from loader.instruments import inst_prop

def columns_rename_tf(data, params, dup):
    data = data[['Cum_PnL', 'Position', 'aPosition', "Total_PnL(USD)", 'Margin', 'Loss', 'Profit']]
    columns_name = {
        'Cum_PnL': f"{params['symbol']}.{params['strategy']}{dup}_Cum_PnL",
        'Position': f"{params['symbol']}.{params['strategy']}{dup}_Position",
        'aPosition': f"{params['symbol']}.{params['strategy']}{dup}_aPosition",
        f"Total_PnL(USD)": f"{params['symbol']}.{params['strategy']}{dup}_Total_PnL",
        'Margin': f"{params['symbol']}.{params['strategy']}{dup}_Margin",
        'Loss': f"{params['symbol']}.{params['strategy']}{dup}_Loss",
        'Profit': f"{params['symbol']}.{params['strategy']}{dup}_Profit",
        }
    return data.rename(columns=columns_name)

def columns_rename_tt(data, params, dup):
    data = data[['Signal', 'Position', 'aPosition']]
    columns_name = {
        'Signal': f"{params['symbol']}.{params['strategy']}{dup}_Signal",
        'Position': f"{params['symbol']}.{params['strategy']}{dup}_Position",
        'aPosition': f"{params['symbol']}.{params['strategy']}{dup}_aPosition",
        }
    return data.rename(columns=columns_name)

def run_backtest(strategy_name, parameters):
    strategies_dict = {
        'rsi_backtest': rsi_backtest,
        # 'bbands_backtest': bbands_backtest,
        # 'stoch_backtest': stoch_backtest,
        # 'stochf_backtest': stochf_backtest,
        # 'stochrsi_backtest': stochrsi_backtest,
        # 'macd_backtest': macd_backtest,
        # 'roc_backtest': roc_backtest,
        'adx_backtest': adx_backtest,
        # 'mom_backtest': mom_backtest,
        'kama_backtest': kama_backtest,
        # 'hilbert_backtest': hilbert_backtest,
        # 'ppo_backtest': ppo_backtest,
        }

    backtest_result = strategies_dict.get(strategy_name)

    return backtest_result(parameters)

def composite_backtest(com_param, symbols, deposit=1000, output_csv=True, plot=True, to_date='', data_source='MT5'):
    for param in com_param:
        if com_param[param]['symbol'] in symbols:
            param = com_param[param]
            break
    if to_date != '':
        param['to_date'] = to_date
    param['data_source'] = data_source
    try:
        results = load_data(param)
        try:
            results.drop(columns=['Open', 'High', 'Low', 'Close', 'Tick_Volume', 'Over_night'], inplace=True)
        except:
            results.drop(columns=['Open', 'High', 'Low', 'Close'], inplace=True)
    except:
        return

    for key, params in com_param.items():
        if params['symbol'] not in symbols:
            print(f"{params['symbol']} unavailable.")
            continue
        try:
            key, dup = key.split('.', 1)
        except:
            dup = ''
        if to_date != '':
            params['to_date'] = to_date
        try:    
            params['cl_stop']
        except:
            params['cl_stop'] = False
        try:
            params['tp_stop']
        except:
            params['tp_stop'] = False
        params['data_source'] = data_source
        params['composite'] = True
        
        result = run_backtest(key, params)
        result['Cum_PnL'] = result['Cum_PnL'] / inst_prop[f"{params['symbol']}"]['pip']

        if not params['trading_mode']:
            try:
                result["Total_PnL(USD)"].fillna(0, inplace=True)
            except:
                result["Total_PnL(USD)"] = 0
                result['Entry_Price'], result['Margin'], result['Loss'], result['Profit'], result['Drawdown'], result['B_Drawdown'], result['B_Peak-to-Trough'] = np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
            result = columns_rename_tf(result, params, dup)
        else:
            result = result[['Signal', 'Position', 'aPosition']]
            result = columns_rename_tt(result, params, dup)

        results = results.join(result)
        
    columns_position = list(results.columns[results.columns.str.contains('_Position')])
    columns_aposition = list(results.columns[results.columns.str.contains('_aPosition')])
    columns_cum_pnl = list(results.columns[results.columns.str.contains('_Cum_PnL')])
    columns_total_pnl = list(results.columns[results.columns.str.contains('_Total_PnL')])
    columns_margin = list(results.columns[results.columns.str.contains('_Margin')])
    columns_loss = list(results.columns[results.columns.str.contains('_Loss')])
    columns_profit = list(results.columns[results.columns.str.contains('_Profit')])
    
    results['Cum_Position'] = results[columns_position].sum(axis=1)
    results['Cum_aPosition'] = results[columns_aposition].sum(axis=1)
    results['Total_Position'] = abs(results[columns_position]).sum(axis=1)
    results['Total_aPosition'] = abs(results[columns_aposition]).sum(axis=1)
    if not param['trading_mode']:
        results['Margins'] = results[columns_margin].sum(axis=1)
        results['Total_Cum_PnL'] = results[columns_cum_pnl].sum(axis=1)
        results['Total_PnL'] = round(results[columns_total_pnl].sum(axis=1), 2)
        results = results.rename(columns={'Total_PnL': f"Total_PnL(USD)"})
        results['Losses'] = results[columns_loss].sum(axis=1)
        results['Profits'] = results[columns_profit].sum(axis=1)
        results['Balance'] = deposit + results['Total_PnL(USD)']
        results.loc[results['Losses'] < 0, 'B_Drawdown'] = calc_drawdown(results['Losses'], balance=results['Balance'], possible_losses=1.2)
        results.loc[results['Losses'] < 0, 'Drawdown'] = calc_drawdown(results['Losses'], balance=deposit, possible_losses=1.2)
        results['Drawdown'].fillna(0, inplace=True)
        b_p2t = []
        b_peak = deposit
        for _, r in results.iterrows():
            if r['Balance'] > b_peak:
                b_peak = r['Balance']
            p2t = -calc_balance_drawdown(r['Balance'], deposit=deposit, peak=b_peak)
            b_p2t.append(p2t)
        results['B_Peak-to-Trough'] = b_p2t
        results['Possible_Losses'] = results['Balance'] + results['Losses']
        results['Possible_Profits'] = results['Balance'] + results['Profits']
    
    try:
        data_dir = path.abspath("") + '/Data/' + data_source + '/Backtest Results/' + to_date + '/'
    except:
        data_dir = path.abspath("") + '/Data/' + data_source + '/Backtest Results/'

    if len(np.unique(np.array(symbols))) == 1:
        symbols = symbols[0] + ' '
    else:
        symbols = 'All '

    if output_csv:
        if not param['trading_mode']:
            file_name = f"check {symbols}composite_backtest {param['timeframe']} (size{str(param['trading_size'])}).csv"
        else:
            file_name = f"check trading mode signal {param['timeframe']} (size{str(param['trading_size'])}).csv"
        try:
            results.to_csv(data_dir + file_name, float_format='%.4f', index=True)
        except (OSError, FileNotFoundError) as e:
            print('Error: ', e)
            print('Creating folder...')
            makedirs(data_dir, exist_ok=True)
            results.to_csv(data_dir + file_name, float_format='%.4f', index=True)
        print(f"Updated '{file_name}'.")

    # Show Plot
    if not param['trading_mode'] and plot:
        print('Loading plot...')
        dlen_f = abs(len(results) - 0)
        dlen_b = 0
        date = results.index.values.tolist()[dlen_b:dlen_f]
        balance = list(results['Balance'])[dlen_b:dlen_f]
        position = list(results['Cum_Position'])[dlen_b:dlen_f]
        aposition = list(results['Cum_aPosition'])[dlen_b:dlen_f]
        t_position = list(results['Total_Position'])[dlen_b:dlen_f]
        t_aposition = list(results['Total_aPosition'])[dlen_b:dlen_f]
        cum_pnl = {}
        for _ in columns_cum_pnl:
            cum_pnl[str(f"{_}")] = list(round(results[f"{_}"], 5))[dlen_b:dlen_f]
        total_cum_pnl = list(results['Total_Cum_PnL'])[dlen_b:dlen_f]
        pnl = list(results[f"Total_PnL(USD)"])[dlen_b:dlen_f]
        margins = list(results['Margins'])[dlen_b:dlen_f]
        p_losses = list(results['Possible_Losses'])[dlen_b:dlen_f]
        p_profits = list(results['Possible_Profits'])[dlen_b:dlen_f]
        drawdown = list(results['Drawdown'])[dlen_b:dlen_f]
        b_drawdown = list(results['B_Drawdown'])[dlen_b:dlen_f]
        # b_p2t = list(results['B_Peak-to-Trough'])[dlen_b:dlen_f]

        down_sampling = False
        if down_sampling:
            div = 500
            date = date[::round((dlen_f - dlen_b) / div)]
            balance = balance[::round((dlen_f - dlen_b) / div)]
            position = position[::round((dlen_f - dlen_b) / div)]
            aposition = aposition[::round((dlen_f - dlen_b) / div)]
            t_position = t_position[::round((dlen_f - dlen_b) / div)]
            t_aposition = t_aposition[::round((dlen_f - dlen_b) / div)]
            for _ in columns_cum_pnl:
                cum_pnl[str(f"{_}")] = cum_pnl[str(f"{_}")][::round((dlen_f - dlen_b) / div)]
            total_cum_pnl = total_cum_pnl[::round((dlen_f - dlen_b) / div)]
            pnl = pnl[::round((dlen_f - dlen_b) / div)]
            margins = margins[::round((dlen_f - dlen_b) / div)]
            p_losses = p_losses[::round((dlen_f - dlen_b) / div)]
            p_profits = p_profits[::round((dlen_f - dlen_b) / div)]
            drawdown = drawdown[::round((dlen_f - dlen_b) / div)]
            b_drawdown = b_drawdown[::round((dlen_f - dlen_b) / div)]
            # b_p2t = b_p2t[::round((dlen_f - dlen_b) / div)]

        fig, ax = plt.subplots(4, figsize=(16, 10), dpi=120, gridspec_kw={'height_ratios': [4, 4, 4, 4]})
        ax0 = ax[0].twinx()
        ax0.bar(date, margins, label='Total Margin(USD)', width=1.0, alpha=0.5, color='turquoise')
        ax0.set_ylabel('Total Margin(USD)')
        ax[0].plot(date, balance, label='Balance(USD)', linewidth=1.0, color='violet')
        ax[0].plot(date, p_losses, label='P_Losses', linewidth=0.7, color='red', alpha=0.5, linestyle='dashed')
        ax[0].set_ylabel('Balance(USD)')
        ax[0].plot(date, p_profits, label='P_Profits', linewidth=0.7, color='green', alpha=0.5, linestyle='dashed')
        ax[1].bar(date, t_aposition, label='Total aPosition', width=1.0, color='black', alpha=0.2)
        ax[1].bar(date, aposition, label='Cum aPosition', width=1.0, color='red')
        ax[1].set_ylabel('aPosition')
        ax2 = ax[2].twinx()
        for _ in columns_cum_pnl:
            ax2.plot(date, cum_pnl[str(f"{_}")], linewidth=0.5, alpha=0.5)
        ax[2].plot(date, total_cum_pnl, label='Total Cum PnL', linewidth=1.0, color='green')
        ax[2].set_ylabel('Total Cum PnL')
        ax2.set_ylabel('Cum PnL')
        ax[3].plot(date, drawdown, label=f"Deposit Drawdown(%)", linewidth=0.5, color='grey')
        ax[3].plot(date, b_drawdown, label=f"Balance Drawdown(%)", linewidth=0.5, color='pink')
        # ax[3].plot(date, b_p2t, label=f"B_Peak-to-Trough(%)", linewidth=0.5, color='pink')
        ax[3].set_ylabel('Drawdown(%)')

        ax[3].fill_between(date, drawdown, color='grey')
        ax[3].fill_between(date, b_drawdown, color='pink')
        # ax[3].fill_between(date, b_p2t, color='pink')

        ax[0].grid(alpha=0.7, color='r', linestyle='-', linewidth=0.2)
        ax[1].grid(alpha=0.7, color='r', linestyle='-', linewidth=0.2)
        ax[2].grid(alpha=0.7, color='r', linestyle='-', linewidth=0.2)
        ax[3].grid(alpha=0.7, color='r', linestyle='-', linewidth=0.2)
        # ax[0].legend()
        ax[1].legend()
        ax[2].legend()
        ax[3].legend()

        f_total_cum_pnl = float('{:.3f}'.format(total_cum_pnl[-1]))
        deposit = round(balance[0])
        f_balance = float('{:.1f}'.format(balance[-1]))
        ymin_total_cum_pnl = float('{:.3f}'.format(min(total_cum_pnl)))
        xmin_total_cum_pnl = date[np.argmin(total_cum_pnl)]
        ymin_balance = float('{:.1f}'.format(min(balance)))
        xmin_balance = date[np.argmin(balance)]
        ymin_drawdown = float('{:.1f}'.format(min(drawdown)))
        xmin_drawdown = date[np.argmin(drawdown)]
        ymin_b_drawdown = float('{:.1f}'.format(min(b_drawdown)))
        xmin_b_drawdown = date[np.argmin(b_drawdown)]
        # ymin_b_p2t = float('{:.1f}'.format(min(b_p2t)))
        # xmin_b_p2t = date[np.argmin(b_p2t)]

        if down_sampling:
            date = date[::round(len(date) / 30)]
        else:
            date = date[::round((dlen_f - dlen_b) / 30)]

        ax[0].set_xticks(date)
        ax[0].set_xticklabels(date)
        ax[1].set_xticks(date)
        ax[1].set_xticklabels(date)
        ax[2].set_xticks(date)
        ax[2].set_xticklabels(date)
        ax[3].set_xticks(date)
        ax[3].set_xticklabels(date)
        fig.autofmt_xdate()
        
        ax[0].annotate(f_balance, (date[-1], f_balance), textcoords='offset points', xytext=(0,-12), ha='left')
        ax[0].annotate(f"deposit={deposit} USD", (date[0], deposit), textcoords='offset points', xytext=(20, 60), ha='center', color='green', bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="g", lw=1))
        ax[0].annotate(f"min={ymin_balance}", (xmin_balance, ymin_balance), textcoords='offset points', xytext=(0,12), ha='center', color='red')
        ax[2].annotate(f_total_cum_pnl, (date[-1], f_total_cum_pnl), textcoords='offset points', xytext=(0,-12), ha='left')
        ax[2].annotate(f"min={ymin_total_cum_pnl}", (xmin_total_cum_pnl, ymin_total_cum_pnl), textcoords='offset points', xytext=(0,12), ha='center', color='red')
        ax[3].annotate(f"max={ymin_drawdown}%", (xmin_drawdown, ymin_drawdown), textcoords='offset points', xytext=(5,0), ha='left', color='black')
        ax[3].annotate(f"max={ymin_b_drawdown}%", (xmin_b_drawdown, ymin_b_drawdown), textcoords='offset points', xytext=(5,0), ha='left', color='pink')
        # ax[3].annotate(f"max={ymin_b_p2t}%", (xmin_b_p2t, ymin_b_p2t), textcoords='offset points', xytext=(5,0), ha='left', color='pink')

        plt_title = f"{symbols}Composite Backtest Results {param['timeframe']} (size{param['trading_size']})"
        plt.suptitle(plt_title)
        plt.tight_layout()
        try:
            fig.savefig(data_dir + f"{plt_title}.png")
        except FileNotFoundError as e:
            print('Error: ', e)
            print('Creating folder...')
            makedirs(data_dir, exist_ok=True)
            fig.savefig(data_dir + f"{plt_title}.png")
        plt.show()
        