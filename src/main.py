from colorama import init, Fore, Style
init()

import data_management as dm
import prediction_tracker as pt
import visualizations as vis
import pandas as pd
from datetime import datetime, timedelta
import sys
import demo
import config
import yfinance as yf

def confirm_action(prompt):
    while True:
        choice = input(f"{prompt} (Y/N): ").upper()
        if choice == 'Y':
            return True
        elif choice == 'N':
            return False
        else:
            print("Invalid input. Please enter Y or N.")

def print_welcome():
    print(Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + "Welcome to the Stock Forecasting Application")
    print(Fore.CYAN + "=" * 50)
    print(Fore.WHITE + "This application allows you to:")
    print("- View and manage a dataset of stocks")
    print("- Make predictions on stock price movements")
    print("- Track prediction accuracy using Brier Score")
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

def display_menu():
    print("\n" + "=" * 30)
    print("MAIN MENU")
    print("=" * 30)
    print("1. View Stocks")
    print("2. Add Stock")
    print("3. Make Prediction")
    print("4. Update Prediction Outcome")
    print("5. View Predictions")
    print("6. View Overall Brier Score")
    print("7. Visualize Stock Prices")
    print("8. Visualize Prediction Accuracy")
    print(Fore.GREEN + "9. Run Demo" + Style.RESET_ALL)
    print("10. Check Real-Time Stock Price")  # New option
    print("11. Clear All Stocks")
    print("12. Exit")
    print("=" * 30)

def handle_choice(choice, stocks=None, predictions=None):
    if stocks is None:
        stocks = dm.load_stock_data()
    if predictions is None:
        predictions = pt.load_predictions()
        predictions = pt.remove_duplicates(predictions)

    if choice == '1':
        display_stocks(stocks)
    elif choice == '2':
        stocks = add_new_stock(stocks)
    elif choice == '3':
        predictions = make_prediction(stocks, predictions)
    elif choice == '4':
        if confirm_action("Do you want to update a prediction outcome?"):
            predictions = update_prediction_outcome(predictions)
            pt.save_all_predictions(predictions)
    elif choice == '5':
        display_predictions(predictions)
    elif choice == '6':
        display_overall_brier_score(predictions)
    elif choice == '7':
        vis.plot_stock_prices(stocks)
    elif choice == '8':
        vis.plot_prediction_accuracy(predictions)
    elif choice == '9':
        demo.run_demo(stocks, predictions)
    elif choice == '10':
        check_real_time_stock_price()
    elif choice == '11':
        if confirm_action("Are you sure you want to clear all stocks? This action cannot be undone."):
            stocks = dm.clear_all_stocks()
            print("All stocks have been cleared.")
    
    return stocks, predictions

def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().upper()
        if user_input in [option.upper() for option in valid_options]:
            return user_input
        print(f"Invalid input. Please choose from {', '.join(valid_options)}.")

def make_prediction(stocks, predictions):
    if confirm_action("Do you want to make a prediction?"):
        try:
            ticker = input("Enter stock ticker: ").upper()
            if ticker not in stocks['Ticker'].values:
                print(f"Error: {ticker} not found in the stock list.")
                return predictions
            
            current_price = stocks.loc[stocks['Ticker'] == ticker, 'Current Price'].values[0]
            print(f"Current price of {ticker}: {current_price}")
            
            prediction = float(input("Enter your prediction (0-1) of stock rising: "))
            if not 0 <= prediction <= 1:
                print("Error: Prediction must be between 0 and 1.")
                return predictions
            
            default_timeframe = config.get_default_timeframe()
            timeframe = get_valid_input(f"Enter timeframe ({default_timeframe}, 3, or 12 months): ", [str(default_timeframe), '3', '12'])
            timeframe = f"{timeframe} month{'s' if timeframe != '1' else ''}"
            
            new_prediction = pt.make_prediction(ticker, prediction, timeframe)
            predictions = pt.add_prediction(predictions, new_prediction)
            pt.save_all_predictions(predictions)
            print("Prediction saved successfully!")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nPrediction making cancelled.")
    return predictions

def display_stocks(stocks):
    if stocks.empty:
        print("No stocks available.")
    else:
        print("\nCurrent Stocks")
        print("--------------")
        print(stocks.to_string(index=False, justify='left'))

def main():
    stocks = dm.load_stock_data()
    predictions = pt.load_predictions()
    predictions = pt.remove_duplicates(predictions)

    print_welcome()

    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == '12':  # Updated exit option
            print("Thank you for using the Stock Forecasting Application. Goodbye!")
            sys.exit()
        
        stocks, predictions = handle_choice(choice, stocks, predictions)
        
        input("\nPress Enter to return to the main menu...")

def add_new_stock(stocks):
    if confirm_action("Do you want to add a new stock?"):
        try:
            ticker = input("Enter stock ticker: ").strip().upper()
            if not ticker:
                raise ValueError("Ticker cannot be empty.")
            
            fetch_method = get_valid_input("Do you want to fetch stock data automatically? (Y/N): ", ['Y', 'N'])
            
            if fetch_method == 'Y':
                try:
                    current_price, company_name = dm.fetch_stock_data(ticker)
                    print(f"Fetched data for {ticker}:")
                    print(f"Company Name: {company_name}")
                    print(f"Current Price: ${current_price:.2f}")
                    if not confirm_action("Is this information correct?"):
                        raise ValueError("User rejected fetched data.")
                except Exception as e:
                    print(f"Error fetching data: {e}")
                    print("Falling back to manual input.")
                    fetch_method = 'N'
            
            if fetch_method == 'N':
                company_name = input("Enter company name: ").strip()
                if not company_name:
                    raise ValueError("Company name cannot be empty.")
                
                current_price = input("Enter current price: ")
                if not current_price.replace('.', '').isdigit():
                    raise ValueError("Price must be a positive number.")
                current_price = float(current_price)
                
                if current_price <= 0:
                    raise ValueError("Price must be greater than zero.")
            
            stocks = dm.add_stock(stocks, ticker, company_name, current_price)
            dm.save_stock_data(stocks)
            print(f"Stock {ticker} added successfully!")
        except Exception as e:
            print(f"Error adding stock: {str(e)}")
    return stocks

def update_prediction_outcome(predictions):
    if predictions.empty:
        print("No predictions available to update.")
        return predictions

    print("\nAvailable predictions to update:")
    updatable_predictions = predictions[predictions['Actual_Outcome'].isna()]
    if updatable_predictions.empty:
        print("No predictions available for update.")
        return predictions

    for index, row in updatable_predictions.iterrows():
        print(f"{index}. {row['Ticker']} - Predicted on {row['Timestamp']}")

    while True:
        try:
            choice = input("\nEnter the number of the prediction you want to update (or 'cancel' to go back): ")
            if choice.lower() == 'cancel':
                return predictions
            choice = int(choice)
            if choice not in updatable_predictions.index:
                raise ValueError("Invalid choice. Please enter a valid number.")
            
            prediction = updatable_predictions.loc[choice]
            actual_outcome = input(f"Enter the actual outcome for {prediction['Ticker']} (0 for down, 1 for up): ")
            if actual_outcome not in ['0', '1']:
                raise ValueError("Invalid input. Please enter 0 or 1.")
            
            actual_outcome = float(actual_outcome)
            predictions.at[choice, 'Actual_Outcome'] = actual_outcome
            predictions.at[choice, 'Brier_Score'] = (prediction['Prediction'] - actual_outcome) ** 2
            print("Prediction updated successfully!")
            break
        except ValueError as e:
            print(f"Error: {str(e)}")

    return predictions

def display_predictions(predictions):
    if predictions.empty:
        print("No predictions available.")
    else:
        print("\nPrediction History")
        print("------------------")
        print(predictions.to_string(index=False))

def display_overall_brier_score(predictions):
    if predictions.empty or predictions['Brier_Score'].isna().all():
        print("No Brier Scores available yet.")
    else:
        overall_score = predictions['Brier_Score'].mean()
        if overall_score < 0.25:
            color = Fore.GREEN
        elif overall_score < 0.5:
            color = Fore.YELLOW
        else:
            color = Fore.RED
        print(f"\nOverall Brier Score: {color}{overall_score:.4f}{Style.RESET_ALL}")
        print("Lower scores indicate better prediction accuracy.")

def check_real_time_stock_price():
    ticker = input("Enter the stock ticker symbol: ").upper()
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = info['currentPrice']
        previous_close = info['previousClose']
        print(f"\nReal-time data for {ticker}:")
        print(f"Current Price: ${current_price:.2f}")
        print(f"Previous Close: ${previous_close:.2f}")
        change = current_price - previous_close
        percent_change = (change / previous_close) * 100
        print(f"Change: ${change:.2f} ({percent_change:.2f}%)")
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")

if __name__ == "__main__":
    main()