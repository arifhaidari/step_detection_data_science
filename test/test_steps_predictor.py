# import pandas as pd
# import pytest
# import joblib
# import sys
# import os

# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  
# MODEL_PATH = os.path.join(PROJECT_ROOT, "../models", "random_forest_model.pkl")

# # to get the current absolute address for importing data_loader, data_processor
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../step_detection_data_science/src")))

# # import my custom classes
# # from steps_predictor import StepPredictor

# from src.steps_predictor import StepPredictor

# @pytest.fixture
# def sample_data():
#      return {
#           "ax_mean": [-0.01708],
#           "ay_mean": [-0.015128],
#           "az_mean": [-1.00284],
#           "gx_mean": [0.0],
#           "gy_mean": [0.77],
#           "gz_mean": [-0.42],
#           "id": ["sample"],
#           "start_time": ["2024-06-14T09:31:04"],
#           "end_time": ["2024-06-14T09:31:05"],
#           "left_steps": [0],
#           "right_steps": [0]
#      }

# def test_predict(sample_data):
#      df = pd.DataFrame(sample_data)
#      predictor = StepPredictor(MODEL_PATH) 
#      predictions = predictor.predict(df)
#      assert "left_steps" in predictions[0]
#      assert "right_steps" in predictions[0]