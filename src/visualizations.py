import matplotlib.pyplot as plt
import pandas as pd
import config

def get_color(color_function):
    try:
        return color_function()
    except:
        print(f"Warning: Could not read color from config file. Using default.")
        return None  # matplotlib will use default color

def plot_stock_prices(stocks):
    plt.figure(figsize=(12, 6))
    prices = stocks['Current Price'].astype(float)
    color = get_color(config.get_stock_price_color)
    bars = plt.bar(stocks['Ticker'], prices, color=color)
    plt.title('Current Stock Prices', fontsize=16)
    plt.xlabel('Stock Ticker', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Annotate each bar with its value
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}',
                 ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

def plot_prediction_accuracy(predictions):
    predictions['Accuracy'] = 1 - predictions['Brier_Score']
    predictions = predictions.dropna(subset=['Accuracy'])
    
    plt.figure(figsize=(10, 6))
    color = config.get_prediction_accuracy_color()
    predictions.groupby('Ticker')['Accuracy'].mean().plot(kind='bar', color=color)
    plt.title('Average Prediction Accuracy by Stock')
    plt.xlabel('Stock Ticker')
    plt.ylabel('Average Accuracy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def create_bar_chart(ax, labels, values, title):
    ax.bar(labels, values)
    ax.set_title(title)
    # Add any other necessary chart formatting
