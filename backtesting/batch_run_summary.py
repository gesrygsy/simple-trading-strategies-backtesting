import pandas as pd
from os import makedirs, path

def batch_run_summary(results, totalnum_strategy, data_source, timeframe):
    for result in results.values():
        symbol = result[0][0]
        strategy_name = result[0][1]
        path_ = path.abspath("") + '/Data/' + data_source + '/Backtest Results/'
        data_dir = path_ + symbol + '/'

        strategy = []
        win_rate = []
        num_trade = []
        total_pnl = []
        pnl_trade = []
        hold_period = []
        pnl_period = []

        for i in result:
            strategy.append(i[2])
            win_rate.append(i[3])
            num_trade.append(i[4])
            total_pnl.append(i[5])
            pnl_trade.append(i[6])
            hold_period.append(i[7])
            pnl_period.append(i[8])

        summary = pd.DataFrame({
            "Strategy": strategy,
            "Win_Rate": win_rate,
            "Num_Trade": num_trade,
            "Total_PnL": total_pnl,
            "PnL_Trade": pnl_trade,
            "Hold_Period": hold_period,
            "PnL_Period": pnl_period,
            })
        
        file_name = f'{symbol}_{strategy_name}_Backtest_Summary {timeframe} ({totalnum_strategy}).csv'
        try:
            summary.to_csv(data_dir + file_name, index=False, float_format='%.4f')
        except Exception as e:
            print('Error: ', e)
            print('Creating folder/file...')
            makedirs(data_dir, exist_ok=True)
            summary.to_csv(data_dir + file_name, index=False, float_format='%.4f')
        finally:
            print(f'Completed {symbol} {strategy_name} {timeframe} Backtest Summary output.')