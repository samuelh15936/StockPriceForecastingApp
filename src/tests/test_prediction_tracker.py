import unittest
import sys
import pandas as pd
from datetime import datetime, timedelta

sys.path.append('..')
import prediction_tracker as pt

class TestPredictionTracker(unittest.TestCase):

    def setUp(self):
        # Create sample predictions for testing
        self.sample_predictions = pd.DataFrame({
            'Ticker': ['AAPL', 'GOOGL', 'MSFT'],
            'Prediction': [0.7, 0.6, 0.8],
            'Timestamp': [datetime.now(), datetime.now() - timedelta(days=1), datetime.now() - timedelta(days=2)],
            'Timeframe': ['3 months', '1 month', '3 months'],
            'Actual_Outcome': [None, 1.0, None],
            'Brier_Score': [None, 0.16, None]
        })

    def test_make_prediction(self):
        prediction = pt.make_prediction('MSFT', 0.8, '3 months')
        self.assertEqual(prediction['Ticker'].iloc[0], 'MSFT')
        self.assertEqual(prediction['Prediction'].iloc[0], 0.8)
        self.assertEqual(prediction['Timeframe'].iloc[0], '3 months')
        self.assertIsInstance(prediction['Timestamp'].iloc[0], pd.Timestamp)
        self.assertIsNone(prediction['Actual_Outcome'].iloc[0])
        self.assertIsNone(prediction['Brier_Score'].iloc[0])

    def test_add_prediction(self):
        new_prediction = pt.make_prediction('NVDA', 0.8, '3 months')
        updated_predictions = pt.add_prediction(self.sample_predictions, new_prediction)
        self.assertEqual(len(updated_predictions), 4)
        self.assertIn('NVDA', updated_predictions['Ticker'].values)
        self.assertTrue(isinstance(updated_predictions['Timestamp'].iloc[-1], pd.Timestamp))

    def test_remove_duplicates(self):
        duplicate = self.sample_predictions.iloc[0].to_dict()
        duplicate['Timestamp'] = pd.Timestamp.now()  # Ensure a different timestamp
        self.sample_predictions = pd.concat([self.sample_predictions, pd.DataFrame([duplicate])], ignore_index=True)
        deduped = pt.remove_duplicates(self.sample_predictions)
        self.assertEqual(len(deduped), 3)  # Changed from 2 to 3

    def test_calculate_brier_score(self):
        prediction = 0.7
        actual_outcome = 1
        brier_score = pt.calculate_brier_score(prediction, actual_outcome)
        self.assertAlmostEqual(brier_score, 0.09)

    # Add more test methods as needed

if __name__ == '__main__':
    unittest.main()
