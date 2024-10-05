# Stock Forecasting Application

## Overview
This application allows users to make predictions on stock price movements for a dataset of stocks. It tracks prediction accuracy using the Brier Score and provides basic performance analysis and visualizations.

## Features
- View and manage a dataset of stocks
- Add new stocks to the dataset
- Make predictions on stock price movements (1, 3, or 12 months timeframe)
- Update prediction outcomes
- Calculate and track prediction accuracy using Brier Score
- Visualize stock prices and prediction accuracy
- Interactive demo mode

## Installation
1. Ensure you have Python 3.7+ installed
2. Clone this repository
3. Create a virtual environment:
   ```python
   python -m venv stockforecast_env
   stockforecast_env\Scripts\activate  # On macOS use `source stockforecast_env/bin/activate`
   ```
4. Install required packages:
   ```pip install -r requirements.txt```

## Usage
1. Run the application:
   ```python src/main.py```
2. Follow the on-screen prompts to navigate the application
3. Use option 9 to run an interactive demo of all features
4. For detailed instructions, refer to the [User Guide](USER_GUIDE.md)

## Testing
This project includes a comprehensive test suite to ensure the reliability and correctness of its functionality. The tests cover various aspects of the application, including data management, prediction tracking, and user interface interactions.

To run the tests:

1. Ensure you're in the project's root directory.
2. Activate your virtual environment if you haven't already:
   ```python
   source stockforecast_env/bin/activate  # On Windows use `stockforecast_env\Scripts\activate`
   ```
3. Run the following command:
   ```python
   python -m unittest discover src/tests
   ```

This command will automatically discover and run all tests in the `src/tests` directory. The output will show you which tests passed, failed, or raised errors.

### What the Tests Cover
- Data Management: Tests for adding, loading, and saving stock data.
- Prediction Tracking: Tests for making predictions, updating outcomes, and calculating Brier scores.
- User Interface: Tests for various menu options and user interactions.
- Visualization: Tests for generating stock price and prediction accuracy visualizations.

### Interpreting Test Results
- A dot (.) indicates a passed test.
- An 'E' indicates an error occurred during the test.
- An 'F' indicates a test failure.

If all tests pass, you'll see a message like "OK" at the end of the output. If any tests fail, you'll see details about the failures, which can help in debugging.

### Note on Warnings
You may see a FutureWarning related to DataFrame concatenation. This warning does not affect the current functionality of the application but is something to be aware of for future updates.

### Extending the Test Suite
If you add new features or modify existing ones, consider adding or updating tests in the `src/tests` directory to maintain the reliability of the application.

## Understanding the Brier Score
The Brier Score measures the accuracy of probabilistic predictions, ranging from 0 to 1. Lower scores indicate better prediction accuracy:
- 0: Perfect prediction
- 0.25: Baseline for random guessing
- 1: Worst possible score

## Configuration
You can customize certain aspects of the application by editing the `config.ini` file. Options include:
- Setting the default prediction timeframe
- Changing visualization colors

For more details on customization, see the [User Guide](USER_GUIDE.md#customizing-the-application).

## Note
This is a prototype version. Future enhancements may include real-time data updates, advanced analytics, and machine learning predictions.

## Documentation
For more detailed information on how to use the Stock Forecasting Application, please refer to our [User Guide](USER_GUIDE.md).
