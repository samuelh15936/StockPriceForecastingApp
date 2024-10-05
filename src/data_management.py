import pandas as pd
import yfinance as yf
from datetime import datetime

def initialize_stock_data():
    """Initialize stock data with 100 stocks."""
    # This is a sample list of 100 stock tickers. You may want to customize this list.
    tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'BRK-B', 'JPM', 'JNJ', 'V', 'PG', 'UNH', 'MA', 'NVDA', 'HD', 'DIS', 'BAC', 'ADBE', 'CRM', 'NFLX', 'CMCSA', 'PFE', 'ABT', 'KO', 'XOM', 'VZ', 'CSCO', 'PEP', 'WMT', 'MRK', 'T', 'INTC', 'NKE', 'PYPL', 'TMO', 'ACN', 'ORCL', 'CVX', 'DHR', 'UNP', 'LIN', 'NEE', 'MDT', 'PM', 'HON', 'BMY', 'QCOM', 'UPS', 'TXN', 'COST', 'LLY', 'AMT', 'SBUX', 'MS', 'RTX', 'C', 'BLK', 'GS', 'IBM', 'MMM', 'BA', 'CAT', 'GE', 'AXP', 'PNC', 'TGT', 'CHTR', 'SPGI', 'BKNG', 'ISRG', 'MO', 'GILD', 'MDLZ', 'TJX', 'CVS', 'CI', 'VRTX', 'ZTS', 'ADP', 'ANTM', 'CCI', 'FIS', 'USB', 'CME', 'COF', 'CL', 'EQIX', 'ICE', 'ATVI', 'AON', 'DD', 'ECL', 'EL', 'EW', 'HUM', 'ITW', 'LRCX', 'MET', 'NSC', 'PLD', 'SYK', 'TFC']
    
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            data.append({
                'Ticker': ticker,
                'Company Name': info['longName'],
                'Current Price': info['currentPrice'],
                'Last Updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except:
            print(f"Error fetching data for {ticker}")
    
    return pd.DataFrame(data)

def add_stock(stocks, ticker, company_name, current_price):
    new_stock = pd.DataFrame({
        'Ticker': [ticker],
        'Company Name': [company_name],
        'Current Price': [f'{current_price:.2f}'],  # Format price with 2 decimal places
        'Last Updated': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    })
    if stocks.empty:
        return new_stock
    else:
        return pd.concat([stocks, new_stock], ignore_index=True)

def update_stock_price(df, ticker, new_price):
    """Update the price of an existing stock."""
    if ticker in df['Ticker'].values:
        df.loc[df['Ticker'] == ticker, 'Current Price'] = new_price
        df.loc[df['Ticker'] == ticker, 'Last Updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        print(f"Stock with ticker {ticker} not found.")
    return df

def save_stock_data(stocks, filename='stocks.csv'):
    """Save the stock data to a CSV file."""
    stocks.to_csv(filename, index=False)
    print(f"Stock data saved to {filename}")

def load_stock_data(filename='stocks.csv'):
    try:
        df = pd.read_csv(filename)
        df['Current Price'] = df['Current Price'].apply(lambda x: f'{float(x):.2f}')
        return df
    except FileNotFoundError:
        print(f"File {filename} not found. Initializing new stock data.")
        return pd.DataFrame(columns=['Ticker', 'Company Name', 'Current Price', 'Last Updated'])

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    current_price = info.get('currentPrice', None)
    company_name = info.get('longName', None)
    if current_price is None or company_name is None:
        raise ValueError("Unable to fetch complete stock data")
    return current_price, company_name

def clear_all_stocks():
    """Clear all stocks from the CSV file and return an empty DataFrame."""
    empty_df = pd.DataFrame(columns=['Ticker', 'Company Name', 'Current Price', 'Last Updated'])
    empty_df.to_csv('stocks.csv', index=False)
    return empty_df
