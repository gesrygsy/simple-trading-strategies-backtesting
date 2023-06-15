import sys

def calc_amount(inst_type):
    if inst_type == 'currency':
        amount = 100000
    else:
        amount = 1
    return amount

def calc_rate(symbol, rate, get_frame):
    if get_frame == 'calc_margin':
        if symbol[-3:] != 'USD':
            rate = 1
    elif get_frame == 'calc_profit':
        if symbol[-3:] == 'USD':
            rate = 1
    elif get_frame == 'calc_profit_cross':
        if symbol[-3:] != 'USD':
            rate = 1 / rate
    return rate

def calc_lotsize(pip, atr, size, timeframe):
    if timeframe == 'H4':
        lotsize = round(pip/(atr*3), 2)
    elif timeframe == 'H1':
        lotsize = round(pip/(atr*12), 2)
    else:
        lotsize = round(pip/atr, 2)
    return round(lotsize*size, 2) if round(lotsize*size, 2) > 0.01 else 0.01

def calc_margin(inst_type, leverage, symbol, rate, lotsize):
    amount = calc_amount(inst_type)
    get_frame = sys._getframe().f_code.co_name
    rate = calc_rate(symbol, rate, get_frame)
    return round(lotsize * amount / leverage * rate, 2)

def calc_profit(inst_type, symbol, level, rate, lotsize):
    amount = calc_amount(inst_type)
    get_frame = sys._getframe().f_code.co_name
    rate = calc_rate(symbol, rate, get_frame)
    return round(lotsize * amount / rate * level, 2)

def calc_profit_cross(inst_type, symbol, level, rate, lotsize):
    amount = calc_amount(inst_type)
    get_frame = sys._getframe().f_code.co_name
    rate = calc_rate(symbol, rate, get_frame)
    return round(lotsize * amount * rate * level, 2)

def calc_drawdown(losses, balance=1000, possible_losses=1.5):
    return round(losses * possible_losses / balance * 100, 1)

def calc_balance_drawdown(c_balance, deposit=1000, peak=1000):
    return round((peak - c_balance) / deposit * 100, 1)