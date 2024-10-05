import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def get_default_timeframe():
    return int(config['General']['default_timeframe'])

def get_stock_price_color():
    return config['Visualization']['stock_price_color']

def get_prediction_accuracy_color():
    return config['Visualization']['prediction_accuracy_color']
