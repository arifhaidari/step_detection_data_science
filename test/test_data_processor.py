import pandas as pd
import pytest
from src.data_processor import DataPreprocessor

@pytest.fixture
def sample_data():
    return {
        "time": [
            "2024-06-14 09:31:04.968000", "2024-06-14 09:31:05.968000", "2024-06-14 09:31:06.968000",
            "2024-06-14 09:31:07.968000", "2024-06-14 09:31:08.968000", "2024-06-14 09:31:09.968000",
            "2024-06-14 09:31:10.968000", "2024-06-14 09:31:11.968000", "2024-06-14 09:31:12.968000",
            "2024-06-14 09:31:13.968000", "2024-06-14 09:31:14.968000", "2024-06-14 09:31:15.968000",
            "2024-06-14 09:31:16.968000", "2024-06-14 09:31:17.968000", "2024-06-14 09:31:18.968000",
            "2024-06-14 09:31:19.968000", "2024-06-14 09:31:20.968000", "2024-06-14 09:31:21.968000",
            "2024-06-14 09:31:22.968000", "2024-06-14 09:31:23.968000"
        ],
        "ax": [-0.01708] * 20,
        "ay": [-0.015128] * 20,
        "az": [-1.00284] * 20,
        "gx": [0.0] * 20,
        "gy": [0.77] * 20,
        "gz": [-0.42] * 20,
        "id": ["sample"] * 20
    }

def test_preprocess(sample_data):
    df = pd.DataFrame(sample_data)
    preprocessor = DataPreprocessor()
    processed_df = preprocessor.preprocess(df)
    
    # Assertions
    assert "time_diff" in processed_df.columns
    assert processed_df.index.name == "time"  # Ensure 'time' is the index
    assert processed_df['time_diff'].dtype == 'float64'  # Ensure 'time_diff' is calculated