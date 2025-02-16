import pytest
import os
import json
import tempfile

from src.data_loader import DataLoader
from src.data_processor import DataPreprocessor
from src.steps_predictor import StepPredictionPipeline, StepPredictor

# Define the model path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  
MODEL_PATH = os.path.join(PROJECT_ROOT, "../models", "random_forest_model.pkl")

import random
from datetime import datetime, timedelta

@pytest.fixture
def sample_data():
     """Generates a list of at least 20 sample data points mimicking sensor input."""
     base_time = datetime(2024, 6, 14, 9, 31, 4, 968000)
     
     data = []
     for i in range(20):  # Generate 20 data points
          data.append({
               "time": (base_time + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S.%f"),
               "metadata": {"side": random.choice(["L", "R"])},
               "ax": round(random.uniform(-0.02, 0.02), 6),
               "ay": round(random.uniform(-0.02, 0.02), 6),
               "az": round(random.uniform(-1.05, -0.95), 6),
               "gx": round(random.uniform(-1.0, 1.0), 2),
               "gy": round(random.uniform(-1.0, 1.0), 2),
               "gz": round(random.uniform(-1.0, 1.0), 2),
          })
     
     return [{"filename": "sample_data.json", "data": data}]


@pytest.fixture
def pipeline(sample_data):
     """Creates a pipeline instance using in-memory sample data."""
     data_loader = DataLoader(sample_data)  # Pass list of JSON files directly
     preprocessor = DataPreprocessor()
     predictor = StepPredictor(MODEL_PATH)
     
     return StepPredictionPipeline(data_loader, preprocessor, predictor)


def test_run(pipeline):
     """Runs the pipeline and verifies the predictions output."""
     predictions = pipeline.run()
     assert isinstance(predictions, list)
     
     if predictions:
          assert "left_steps" in predictions[0]
          assert "right_steps" in predictions[0]













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


# import pytest
# import json
# from src.data_loader import DataLoader
# from src.data_processor import DataPreprocessor
# from src.steps_predictor import StepPredictionPipeline, StepPredictor

# @pytest.fixture
# def pipeline(tmp_path):
#      # Create a temporary directory
#      test_data_dir = tmp_path / "test_data"
#      test_data_dir.mkdir()

#      # Define sample JSON content
#      sample_json_data = [
#           {
#                "time": "2024-06-14 09:31:04.968000",
#                "metadata": {"side": "L"},
#                "ax": -0.01708,
#                "gz": -0.42,
#                "gx": 0.0,
#                "az": -1.00284,
#                "gy": 0.77,
#                "ay": -0.015128
#           }
#      ]

#      # Create a sample JSON file in the directory
#      test_file = test_data_dir / "sample_data.json"
#      with open(test_file, "w") as f:
#           json.dump(sample_json_data, f)

#      # Initialize components
#      data_loader = DataLoader(str(test_data_dir))  # Pass directory path
#      preprocessor = DataPreprocessor()
#      predictor = StepPredictor(MODEL_PATH)
     
#      return StepPredictionPipeline(data_loader, preprocessor, predictor)

