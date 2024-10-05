import pandas as pd
from datetime import datetime
import pandas as pd  # Added import for pd.Timestamp

def add_prediction(predictions, new_prediction):
    if isinstance(new_prediction, pd.DataFrame):
        new_pred_df = new_prediction
    else:
        new_pred_df = pd.DataFrame([new_prediction])
    
    if predictions.empty:
        return new_pred_df
    else:
        # Ensure all columns from both DataFrames are included
        all_columns = list(set(predictions.columns) | set(new_pred_df.columns))
        
        # Reindex both DataFrames with all columns, filling missing values with None
        predictions_reindexed = predictions.reindex(columns=all_columns, fill_value=None)
        new_pred_df_reindexed = new_pred_df.reindex(columns=all_columns, fill_value=None)
        
        # Concatenate the reindexed DataFrames
        combined = pd.concat([predictions_reindexed, new_pred_df_reindexed], axis=0, ignore_index=True)
        return remove_duplicates(combined)

def make_prediction(ticker, prediction, timeframe):
    return pd.DataFrame({
        'Ticker': [ticker],
        'Prediction': [prediction],
        'Timestamp': [pd.Timestamp.now()],
        'Timeframe': [timeframe],
        'Actual_Outcome': [None],
        'Brier_Score': [None]
    })

def save_prediction(prediction, filename='predictions.csv'):
    """Save a prediction to a CSV file."""
    df = pd.DataFrame([prediction])
    df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)

def load_predictions(filename='predictions.csv'):
    """Load predictions from a CSV file."""
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Ticker', 'Prediction', 'Timeframe', 'Timestamp', 'Actual_Outcome', 'Brier_Score'])

def calculate_brier_score(prediction, actual_outcome):
    """Calculate the Brier Score for a single prediction."""
    return (prediction - actual_outcome) ** 2

def update_prediction_outcome(predictions, ticker, actual_outcome):
    """Update the actual outcome and calculate Brier Score for a prediction."""
    if ticker in predictions['Ticker'].values:
        mask = (predictions['Ticker'] == ticker) & (predictions['Actual_Outcome'].isnull())
        if mask.any():
            predictions.loc[mask, 'Actual_Outcome'] = actual_outcome
            predictions.loc[mask, 'Brier_Score'] = predictions.loc[mask, 'Prediction'].apply(lambda x: calculate_brier_score(x, actual_outcome))
        else:
            print(f"No open predictions found for {ticker}")
    else:
        print(f"No predictions found for {ticker}")
    return predictions

def save_all_predictions(predictions, filename='predictions.csv'):
    """Save all predictions to a CSV file."""
    predictions.to_csv(filename, index=False)

def remove_duplicates(predictions):
    if predictions.empty:
        return predictions
    
    # Convert 'Timestamp' column to datetime
    predictions['Timestamp'] = pd.to_datetime(predictions['Timestamp'])
    
    predictions = predictions.sort_values('Timestamp', ascending=False)
    predictions = predictions.drop_duplicates(subset=['Ticker', 'Timeframe'], keep='first')
    return predictions.reset_index(drop=True)

def clear_all_predictions():
    """Clear all predictions and return an empty DataFrame."""
    empty_df = pd.DataFrame(columns=['Ticker', 'Prediction', 'Timeframe', 'Timestamp', 'Actual_Outcome', 'Brier_Score'])
    empty_df.to_csv('predictions.csv', index=False)
    return empty_df
