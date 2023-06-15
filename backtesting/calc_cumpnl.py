from loader.calculators import calc_lotsize

import pandas as pd

def position_reset():
    position = 0
    aposition = 0
    period = 0
    d_clr = 0
    d_tpr = 0
    return position, aposition, period, d_clr, d_tpr

def signal_t(row):
    try:
        signal = row['Signal_T']
    except:
        signal = row['Signal']
    return signal

def calc_cumpnl(row, param, position_rs, aposition_rs, trade_pol_rs, period_rs, d_clr_rs, d_tpr_rs, cum_pnl_rs):
    
    if position_rs != 0:
        position = position_rs
    else:
        position = 0
        trade_pol_rs = 0
    if aposition_rs != 0:
        aposition = aposition_rs
    else:
        aposition = 0
        trade_pol_rs = 0

    position_long = lambda x: x+1 if x<1 else 1
    position_short = lambda x: x-1 if x>-1 else -1

    try:
        over_night = row['Over_night']
    except:
        over_night = 0

    if param['strategy'] in ['MOM', 'RSI', 'MFI']:
        if (row['Signal_T'] == 1) & ~pd.isna(row[f"MA{param['period_ma']}"]) & ~pd.isna(row[f"ATR{param['atr']}"]) & (position != 1) & (over_night == 0):
            position = position_long(position)
            aposition = position * calc_lotsize(param['pip'], row[f"ATR{param['atr']}"], param['trading_size'], param['timeframe'])

        if (row['Signal_T'] == -1) & ~pd.isna(row[f"MA{param['period_ma']}"]) & ~pd.isna(row[f"ATR{param['atr']}"]) & (position != -1) & (over_night == 0):
            position = position_short(position)
            aposition = position * calc_lotsize(param['pip'], row[f"ATR{param['atr']}"], param['trading_size'], param['timeframe'])

    elif param['strategy'] in ['MACD', 'Stoch', 'Stochf', 'StochRSI', 'PPO']:
        if (row['Signal'] == 1) & ~pd.isna(row[f"ATR{param['atr']}"]) & (position != 1) & (over_night == 0):
            position = position_long(position)
            aposition = position * calc_lotsize(param['pip'], row[f"ATR{param['atr']}"], param['trading_size'], param['timeframe'])
        if (row['Signal'] == -1) & ~pd.isna(row[f"ATR{param['atr']}"]) & (position != -1) & (over_night == 0):
            position = position_short(position)
            aposition = position * calc_lotsize(param['pip'], row[f"ATR{param['atr']}"], param['trading_size'], param['timeframe'])
    
    elif param['strategy'] in ['KAMA', 'Hilbert']:
        if param['cross_tp']:
            if (row['Signal'] == 1) & ~pd.isna(row[f"MA{param['period_ma']}"]) & ~pd.isna(row[f"ATR{param['atr']}"]) & (position != 1) & (over_night == 0):
                position = position_long(position)
                aposition = position * calc_lotsize(param['pip'], row[f"ATR{param['atr']}"], param['trading_size'], param['timeframe'])
            if (row['Signal'] == -1) & ~pd.isna(row[f"MA{param['period_ma']}"]) & ~pd.isna(row[f"ATR{param['atr']}"]) & (position != -1) & (over_night == 0):
                position = position_short(position)
                aposition = position * calc_lotsize(param['pip'], row[f"ATR{param['atr']}"], param['trading_size'], param['timeframe'])
        else:
            if (row['Signal'] == 1) & ~pd.isna(row[f"MA{param['period_ma']}"]) & ~pd.isna(row[f"ATR{param['atr']}"]) & (position != 1) & (over_night == 0):
                position = position_long(position)
                aposition = position * calc_lotsize(param['pip'], row[f"ATR{param['atr']}"], param['trading_size'], param['timeframe'])
            if (row['Signal'] == -1) & ~pd.isna(row[f"MA{param['period_ma']}"]) & ~pd.isna(row[f"ATR{param['atr']}"]) & (position != -1) & (over_night == 0):
                position = position_short(position)
                aposition = position * calc_lotsize(param['pip'], row[f"ATR{param['atr']}"], param['trading_size'], param['timeframe'])
    
    else:
        if (row['Signal'] == 1) & ~pd.isna(row[f"MA{param['period_ma']}"]) & ~pd.isna(row[f"ATR{param['atr']}"]) & (position != 1) & (over_night == 0):
            position = position_long(position)
            aposition = position * calc_lotsize(param['pip'], row[f"ATR{param['atr']}"], param['trading_size'], param['timeframe'])
        
        if (row['Signal'] == -1) & ~pd.isna(row[f"MA{param['period_ma']}"]) & ~pd.isna(row[f"ATR{param['atr']}"]) & (position != -1) & (over_night == 0):
            position = position_short(position)
            aposition = position * calc_lotsize(param['pip'], row[f"ATR{param['atr']}"], param['trading_size'], param['timeframe'])

    pnl = aposition_rs * row['Price_Diff']
    trade_pol = trade_pol_rs + pnl

    d_clr = row[f"CLr{param['cl_ratio']}"] * ((param['decay'] - period_rs) / param['decay']) * abs(position) * param['trading_size']

    pol_oh = round(trade_pol_rs + (aposition_rs * (row['High'] - row['Open'])), 6)
    pol_ol = round(trade_pol_rs + (aposition_rs * (row['Low'] - row['Open'])), 6)

    if (param['strategy'] in ['KAMA', 'Hilbert']) and param['cross_tp']:
        d_tpr = row['Cross_Close'] * param['trading_size'] * abs(position)

        if (trade_pol < d_clr_rs) and (signal_t(row) != position) and (over_night == 0):
            position, aposition, period, d_clr, d_tpr = position_reset()
        if (position_rs == 1 and d_tpr_rs < 0) or (position_rs == -1 and d_tpr_rs > 0) and (over_night == 0):
            position, aposition, period, d_clr, d_tpr = position_reset()
    else:
        if not param['trailing_stop']:
            d_tpr = row[f"TPr{param['tp_ratio']}"] * ((param['decay'] - period_rs) / param['decay']) * abs(position) * param['trading_size']
        else:
            d_tpr = row[f"TPr{param['tp_ratio']}"] * abs(position) * param['trading_size']

        if (trade_pol < d_clr_rs) and (signal_t(row) != position) and (over_night == 0):
            position, aposition, period, d_clr, d_tpr = position_reset()
        if (trade_pol > d_tpr_rs) and (position_rs != 0) and (over_night == 0):
            position, aposition, period, d_clr, d_tpr = position_reset()

    if (param['cl_stop']) and ((d_clr > pol_oh) or (d_clr > pol_ol)) and (position != 0):
        pnl = (d_clr - trade_pol_rs) * abs(position)
        trade_pol = trade_pol_rs * abs(position) + pnl
        position, aposition, period, d_clr, d_tpr = position_reset()
    if (param['tp_stop']) and ((pol_oh > d_tpr) or (pol_ol > d_tpr)) and (position != 0):
        pnl = (d_tpr - trade_pol_rs) * abs(position)
        trade_pol = trade_pol_rs * abs(position) + pnl
        position, aposition, period, d_clr, d_tpr = position_reset()

    cum_pnl = cum_pnl_rs + pnl

    if (trade_pol != 0):
        period = period_rs + 1
    else:
        period = 0

    return position, aposition, trade_pol, period, pnl, d_clr, d_tpr, cum_pnl