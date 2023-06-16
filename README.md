# simple-trading-strategies-backtesting
-----

A simple trading strategies backtest tool for forex.

## Pre requisites
To get this tool working is necessary to install some packages.
```python
pip install -r requirements.txt
```
And you have to install TA-Lib library manually.

## Quickstart

```python
from backtesting.backtest_adx import adx_backtest

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

adx_backtest(adx_backtest_param)
```

## Composite backtesting

You can backtesting with multiple symbols and strategies. Put a json file which contains multiple parameters you like to backtest. It should be in `./parameters/{data_source}/{symbol}_composite_parameters ({timeframe}).json`.

```python
from backtesting.backtest_composite import composite_backtest
from loader.param_reader import import_composite_param

symbol = 'EURUSD' # or 'All'
timeframe = 'Daily'
data_source = 'MT5'

composite_param, symbols = import_composite_param(symbol=symbol, trading_mode=False, trading_size=0.05, timeframe=timeframe, data_source=data_source)
composite_backtest(composite_param, symbols, deposit=5000, output_csv=True, data_source=data_source, to_date='', plot=True)
```

![testing strategies on EURUSD](Data/MT5/Backtest%20Results/EURUSD%20Composite%20Backtest%20Results%20Daily%20(size0.05).png)

## Batch backtesting

It also support batch backtesting with multiple cores CPU. It should outputs a results summary with csv file.

```python
import numpy as np
from backtesting.backtest_rsi import rsi_backtest

symbols = ['EURUSD']
timeframe = ['Daily']
data_source = ['MT5']

# All pairs value datatype of batch_param should be a list
batch_param = {
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

rsi_backtest(batch_param)
```

## Disclaimer

This tool is for research purposes, use the tool at your own risk. The authors assume no responsibility for your trading results.