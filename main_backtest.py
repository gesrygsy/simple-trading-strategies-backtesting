import numpy as np

from backtesting.backtest_adx import adx_backtest
from backtesting.backtest_kama import kama_backtest
from backtesting.backtest_rsi import rsi_backtest
from backtesting.backtest_composite import composite_backtest
from loader.param_reader import import_composite_param

symbols = ['EURUSD']
symbol = 'EURUSD'
timeframe = 'Daily'
data_source = 'MT5'

adx_backtest_param = {
    'symbol': symbol,
    'timeframe': timeframe,
    'strategy': 'ADX', # strategy name
    'period': 20, # strategy indicator period
    'period_ma': 120, # strategy indicator MovingAverage period
    'period_ro': 4, # strategy indicator Rolling period
    'threshold': 15, # threshold used to trigger signals
    'atr': 14, # AverageTrueRange to calculate trading entry size for every timeperiod
    'trading_size': 0.05, # trading size
    'cl_ratio': 1.0, # CutLoss (StopLoss) ratio, depend on value of atr
    'tp_ratio': 1.0, # TakeProfit ratio, depend on value of atr
    'cl_stop': False,
    'tp_stop': False,
    'decay': 10, # the time period represent cl_ratio & tp_ratio decay
    'trailing_stop': True, # if True, the decay period wouldn't apply to tp_ratio
    'show_plt': True, # if True, plot the backtest results
    'trading_mode': False, # Set to False
    'data_source': data_source,
    }

adx_batch_param = {
    'symbol': symbols,
    'timeframe': [timeframe],
    'strategy': ['ADX'],
    'period': list(range(14, 21)),
    'period_ma': list(range(80, 151, 5)),
    'period_ro': list(range(3, 6)),
    'threshold': list(np.linspace(15, 25, num=3, endpoint=True)),
    'atr': [14],
    'trading_size': [0.05],
    'cl_ratio': list(np.linspace(1.0, 2.0, num=3, endpoint=True)),
    'tp_ratio': list(np.linspace(1.0, 2.0, num=3, endpoint=True)),
    'cl_stop': [False],
    'tp_stop': [False],
    'decay': list(range(5, 11, 5)),
    'trailing_stop': [True],
    'data_source': [data_source],
}

kama_backtest_param = {
    'symbol': symbol,
    'timeframe': timeframe,
    'strategy': 'KAMA',
    'period': 25,
    'period_ma': 33,
    'atr': 14,
    'trading_size': 0.05,
    'cl_ratio': 1.5,
    'tp_ratio': 2.0,
    'cl_stop': False,
    'tp_stop': False,
    'decay': 5,
    'trailing_stop': True,
    'cross_tp': False,
    'batch_run': False,
    'show_plt': True,
    'trading_mode': False,
    'data_source': data_source,
    }

kama_batch_param = {
    'symbol': symbols,
    'timeframe': [timeframe],
    'strategy': ['KAMA'],
    'period': list(range(16, 26)),
    'period_ma': list(range(25, 41, 2)),
    'atr': [14],
    'trading_size': [0.05],
    'cl_ratio': list(np.linspace(1.0, 2.0, num=3, endpoint=True)), 
    'tp_ratio': list(np.linspace(1.0, 2.0, num=3, endpoint=True)),
    'cl_stop': [False],
    'tp_stop': [False],
    'trailing_stop': [True], 
    'cross_tp': [False],
    'decay': list(range(5, 11, 5)),
    'data_source': [data_source],
}

rsi_backtest_param = {
    'symbol': symbol,
    'timeframe': timeframe,
    'strategy': 'RSI',
    'period': 9,
    'period_ma': 115,
    'rsi_range': 15,
    'atr': 14,
    'trading_size': 0.05,
    'cl_ratio': 1.0,
    'tp_ratio': 2.0,
    'cl_stop': False,
    'tp_stop': False,
    'decay': 5,
    'trailing_stop': True,
    'batch_run': False,
    'show_plt': True,
    'trading_mode': False,
    'data_source': data_source,
    }

rsi_batch_param = {
    'symbol': symbols,
    'timeframe': [timeframe],
    'strategy': ['RSI'],
    'period': list(range(7, 16)),
    'period_ma': list(range(50, 151, 5)),
    'rsi_range': list(range(15, 26, 5)),
    'atr': [14],
    'trading_size': [0.05],
    'cl_ratio': list(np.linspace(1.0, 2.0, num=3, endpoint=True)), 
    'tp_ratio': list(np.linspace(1.0, 2.0, num=3, endpoint=True)),
    'cl_stop': [False],
    'tp_stop': [False],
    'decay': list(range(5, 11, 5)),
    'trailing_stop': [True],
    'data_source': [data_source],
}

def main():
    # adx_backtest(adx_backtest_param)
    # adx_backtest(adx_batch_param)

    # kama_backtest(kama_backtest_param)
    # kama_backtest(kama_batch_param)

    # rsi_backtest(rsi_backtest_param)
    # rsi_backtest(rsi_batch_param)

    # composite_param, symbols = import_composite_param(symbol='EURUSD', trading_mode=False, trading_size=0.05, timeframe=timeframe, data_source=data_source)
    # composite_backtest(composite_param, symbols, deposit=5000, output_csv=True, data_source=data_source, to_date='', plot=True)

    print('Completed.')

if __name__ == '__main__':
    main()
