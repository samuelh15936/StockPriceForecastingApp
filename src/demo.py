# src/demo.py

import time
import main
import data_management as dm
import prediction_tracker as pt
from unittest.mock import patch

def clear_data_for_demo(stocks, predictions):
    print("Clearing all stocks and predictions for demo purposes...")
    return dm.clear_all_stocks(), pt.clear_all_predictions()

def run_demo(stocks, predictions):
    stocks, predictions = clear_data_for_demo(stocks, predictions)
    print("Welcome to the Stock Forecasting Application Demo!")
    input("Press Enter to start the demo...")

    steps = [
        ("Viewing Current Stocks", "1"),
        ("Adding a New Stock (Manual Input)", "2"),
        ("Adding a New Stock (Automatic Fetch)", "2"),
        ("Making a Prediction", "3"),
        ("Viewing Predictions", "5"),
        ("Updating a Prediction Outcome", "4"),
        ("Viewing Overall Brier Score", "6"),
        ("Visualizing Stock Prices", "7"),
        ("Visualizing Prediction Accuracy", "8"),
        ("Checking Real-Time Stock Price", "10")
    ]

    for i, (step_description, option) in enumerate(steps, 1):
        print(f"\nStep {i}: {step_description}")
        input(f"Press Enter to select option {option}...")

        if step_description == "Adding a New Stock (Manual Input)":
            ticker = input("Enter stock ticker for manual input: ")
            company_name = input("Enter company name: ")
            price = input("Enter current price: ")
            with patch('builtins.input', side_effect=['Y', ticker, 'N', company_name, price]):
                stocks, predictions = main.handle_choice(option, stocks, predictions)
        elif step_description == "Adding a New Stock (Automatic Fetch)":
            ticker = input("Enter stock ticker for automatic fetch: ")
            with patch('builtins.input', side_effect=['Y', ticker, 'Y', 'Y']):
                stocks, predictions = main.handle_choice(option, stocks, predictions)
        elif step_description == "Making a Prediction":
            ticker = input("Enter stock ticker for prediction: ")
            prediction = input("Enter prediction (0-1): ")
            timeframe = input("Enter timeframe (1, 3, or 12 months): ")
            with patch('builtins.input', side_effect=['Y', ticker, prediction, timeframe]):
                stocks, predictions = main.handle_choice(option, stocks, predictions)
        elif step_description == "Updating a Prediction Outcome":
            with patch('builtins.input', side_effect=['Y', '0', '1']):
                stocks, predictions = main.handle_choice(option, stocks, predictions)
        elif step_description == "Checking Real-Time Stock Price":
            ticker = input("Enter stock ticker for real-time price check: ")
            with patch('builtins.input', return_value=ticker):
                stocks, predictions = main.handle_choice(option, stocks, predictions)
        else:
            stocks, predictions = main.handle_choice(option, stocks, predictions)

        time.sleep(2)  # Pause for 2 seconds between steps

    print("\nDemo Complete! Thank you for exploring the Stock Forecasting Application.")

if __name__ == "__main__":
    run_demo()
