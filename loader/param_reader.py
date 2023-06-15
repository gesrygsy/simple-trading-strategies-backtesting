import json

def import_composite_param(symbol='All', trading_mode=False, trading_size=0.01, timeframe='Daily', data_source='AlphaVantage'):
    try:
        symbol = symbol + '_'
        file_name = f"parameters/{data_source}/{symbol}composite_parameters ({timeframe}).json"
        symbols = []
        with open(file_name) as f:
            file = f.read()
            composite_param = json.loads(file)
        for key, values in composite_param.items():
            symbols.append(values['symbol'])
            composite_param[key]['trading_mode'] = trading_mode
            composite_param[key]['batch_run'] = False
            composite_param[key]['show_plt'] = False
            composite_param[key]['trading_size'] = trading_size
        return composite_param, symbols
    except Exception as e:
        print(f'ERROR: {e}')
        quit()
