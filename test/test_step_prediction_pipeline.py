# import pytest

# import sys
# import os

# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  
# MODEL_PATH = os.path.join(PROJECT_ROOT, "../models", "random_forest_model.pkl")


# from src.data_loader import DataLoader
# from src.data_processor import DataPreprocessor
# from src.steps_predictor import StepPredictionPipeline, StepPredictor

# @pytest.fixture
# def pipeline():
#      data_loader = DataLoader("test_data")
#      preprocessor = DataPreprocessor()
#      predictor = StepPredictor(MODEL_PATH)
#      return StepPredictionPipeline(data_loader, preprocessor, predictor)

# def test_run(pipeline):
#      predictions = pipeline.run()
#      assert isinstance(predictions, list)
#      if predictions:
#           assert "left_steps" in predictions[0]
#           assert "right_steps" in predictions[0]