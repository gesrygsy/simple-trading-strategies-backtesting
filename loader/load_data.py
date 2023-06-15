from os import path
import pandas as pd
import numpy as np

def load_data(param):
    data_source = str(param['data_source'])
    try:
        to_date = str(param['to_date']) + '/'
    except:
        to_date = ''
    symbol = param['symbol']
    timeframe = param['timeframe']
    try:
        trading_mode = param['trading_mode']
    except:
        trading_mode = False

    path_ = path.abspath("") + '/Data/' + data_source + '/' + to_date
    data_dir = path_ + symbol + '/'

    try:
        file = data_dir + f"{symbol}_{timeframe}.csv"
        df = pd.read_csv(file, index_col=0)
        
    except FileNotFoundError as e:
        print('Error: ', e)

        try:
            print('Try reading json file...')
            file = data_dir + f"{symbol}_{timeframe}.json"
            # with open(file) as f:
            #     df = json.load(f)
            df = pd.read_json(file, dtype={'Open': 'float32', 'Low': 'float32', 'High': 'float32', 'Close': 'float32'})
        except FileNotFoundError as e:
            print('Error: ', e)
            quit()

    if trading_mode:
        df = df.tail(1200)

    if timeframe == 'H4':
        df['Over_night'] = pd.to_datetime(df.index)
        df['Over_night'] = df['Over_night'].dt.day - df['Over_night'].dt.day.shift(1)

    return df

def load_today_positions(data):
    today_total_position = list(data['Total_Position'])[-1]
    today_total_aposition = list(data['Total_aPosition'])[-1]

    for columns in ['_Signal', '_Position']:
        drop_signal_columns = list(data.columns[data.columns.str.contains(columns)])
        data.drop(columns=drop_signal_columns, inplace=True)

    data.drop(columns=['Cum_aPosition', 'Total_aPosition'], inplace=True)
    today_positions = {}
    symbol_sets = [column.split('.')[0] for column in data.columns.to_numpy()]

    for symbol in np.unique(symbol_sets):
        item_dict = {}
        for item in list(data.columns[data.columns.str.contains(symbol)]):
            item_dict[item.split('.')[1].split('_')[0]] = data[item].to_list()[-1]
        today_positions[symbol] = item_dict

    return today_positions, today_total_position, today_total_aposition
