import pandas as pd
import pytest
import joblib
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  
MODEL_PATH = os.path.join(PROJECT_ROOT, "../models", "random_forest_model.pkl")

from src.steps_predictor import StepPredictor

@pytest.fixture
def sample_data():
     return {
          "time": ["2024-06-14 09:31:04.968000", "2024-06-14 09:31:05.968000"],
          "ax": [-0.01708, -0.01708],
          "ay": [-0.015128, -0.015128],
          "az": [-1.00284, -1.00284],
          "gx": [0.0, 0.0],
          "gy": [0.77, 0.77],
          "gz": [-0.42, -0.42],
          "id": ["sample", "sample"],
          "side": ["L", "R"]
     }

def test_predict(sample_data):
     df = pd.DataFrame(sample_data)
     predictor = StepPredictor(MODEL_PATH)
     predictions = predictor.predict(df)
     assert "left_steps" in predictions[0]
     assert "right_steps" in predictions[0]