# src/demo.py

import time
import main
from unittest.mock import patch

def run_demo(stocks, predictions):
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
            with patch('builtins.input', side_effect=['DEMO', 'N', 'Demo Company', '100.00']):
                stocks, predictions = main.handle_choice(option, stocks, predictions)
        elif step_description == "Adding a New Stock (Automatic Fetch)":
            with patch('builtins.input', side_effect=['AAPL', 'Y', 'Y']):
                stocks, predictions = main.handle_choice(option, stocks, predictions)
        elif step_description == "Checking Real-Time Stock Price":
            with patch('builtins.input', return_value='AAPL'):
                stocks, predictions = main.handle_choice(option, stocks, predictions)
        else:
            stocks, predictions = main.handle_choice(option, stocks, predictions)

        time.sleep(2)  # Pause for 2 seconds between steps

    print("\nDemo Complete! Thank you for exploring the Stock Forecasting Application.")

if __name__ == "__main__":
    run_demo()
