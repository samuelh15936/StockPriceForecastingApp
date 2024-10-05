# Stock Forecasting Application User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Main Menu Options](#main-menu-options)
4. [Making a Prediction](#making-a-prediction)
5. [Updating a Prediction Outcome](#updating-a-prediction-outcome)
6. [Checking Real-Time Stock Prices](#checking-real-time-stock-prices)
7. [Understanding the Brier Score](#understanding-the-brier-score)
8. [Visualizations](#visualizations)
9. [Demo Mode](#demo-mode)
10. [Customizing the Application](#customizing-the-application)

## Introduction
The Stock Forecasting Application is a tool that allows users to make predictions on stock price movements, track prediction accuracy, visualize stock data, and check real-time stock prices. This guide will walk you through the various features of the application.

## Getting Started
1. Ensure you have Python 3.7+ installed on your system.
2. Install the required packages by running `pip install -r requirements.txt` in the project directory.
3. Run the application by executing `python src/main.py` in your terminal.

## Main Menu Options
1. View Stocks: Display the current list of stocks in the dataset.
2. Add Stock: Add a new stock to the dataset.
3. Make Prediction: Make a prediction for a stock's price movement.
4. Update Prediction Outcome: Update the outcome of a previous prediction.
5. View Predictions: See all your predictions and their outcomes.
6. View Overall Brier Score: Check your overall prediction accuracy.
7. Visualize Stock Prices: See a graph of stock prices.
8. Visualize Prediction Accuracy: See a graph of your prediction accuracy over time.
9. Run Demo: Start an interactive demo of all features.
10. Check Real-Time Stock Price: Get current price information for a specific stock.
11. Exit: Close the application.

## Adding a New Stock
1. Select option 2 from the main menu.
2. Enter the stock ticker symbol when prompted.
3. Choose whether to fetch stock data automatically:
   - If you select 'Y', the application will attempt to fetch the current price and company name using yfinance.
   - If the data is fetched successfully, you'll be shown the information and asked to confirm if it's correct.
   - If there's an error fetching the data or you reject the fetched information, you'll be prompted to enter the data manually.
   - If you select 'N', you'll be prompted to enter the company name and current stock price manually.
4. The new stock will be added to your dataset.

This feature allows you to quickly add new stocks to your dataset with up-to-date information from yfinance, saving time and reducing the chance of data entry errors.

## Making a Prediction
1. Select option 3 from the main menu.
2. Enter the stock ticker symbol when prompted.
3. Enter your prediction (0-1) for the likelihood of the stock rising.
4. Choose a timeframe (1, 3, or 12 months).

## Updating a Prediction Outcome
1. Select option 4 from the main menu.
2. Choose the prediction you want to update from the list.
3. Enter the actual outcome (0 for down, 1 for up).

## Checking Real-Time Stock Prices
1. Select option 10 from the main menu.
2. Enter the stock ticker symbol when prompted.
3. The application will display:
   - Current Price
   - Previous Close
   - Price Change (in dollars and percentage)

This feature allows you to get up-to-date price information for any stock, helping you make more informed predictions.

## Understanding the Brier Score
The Brier Score measures prediction accuracy, ranging from 0 (perfect predictions) to 1 (worst possible predictions). A score of 0.25 represents random guessing. Lower scores indicate better prediction accuracy.

## Visualizations
- Stock Prices: Option 7 displays a bar chart of current stock prices.
- Prediction Accuracy: Option 8 shows a bar chart of average prediction accuracy by stock.

## Demo Mode
Select option 9 from the main menu to run an interactive demo that walks you through all the features of the application.

## Customizing the Application
You can customize certain aspects of the application by editing the `config.ini` file in the project root directory:
- Set the default prediction timeframe
- Change the colors used in visualizations

Example `config.ini`:
```
[General]
default_timeframe = 3

[Visualization]
stock_price_color = blue
prediction_accuracy_color = green
```

Editing these values will allow you to personalize your experience with the Stock Forecasting Application.
