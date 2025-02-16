import pandas as pd
import pytest
import sys

# to get the current absolute address for importing data_loader, data_processor
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../step_detection_data_science/src")))

# import my custom classes
# from data_processor import FeatureExtractor

from src.data_processor import FeatureExtractor

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

def test_extract_features(sample_data):
     df = pd.DataFrame(sample_data)
     features_df = FeatureExtractor.extract_features(df)
     assert "ax_mean" in features_df.columns
     assert "left_steps" in features_df.columns
     assert "right_steps" in features_df.columns
     assert len(features_df) == 1