import os
import json
import pandas as pd
import pytest
import sys

# to get the current absolute address for importing data_loader, data_processor (without container)
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../step_detection_data_science/src")))

# import my custom classes
# from data_loader import DataLoader

# with container
from src.data_loader import DataLoader

@pytest.fixture
def test_dir():
     print('test is here 1')
     test_dir = "test_data"
     os.makedirs(test_dir, exist_ok=True)
     sample_data = [
          {
               "time": "2024-06-14 09:31:04.968000",
               "metadata": {"side": "L"},
               "ax": -0.01708,
               "gz": -0.42,
               "gx": 0.0,
               "az": -1.00284,
               "gy": 0.77,
               "ay": -0.015128
          }
     ]
     sample_file = os.path.join(test_dir, "sample.json")
     with open(sample_file, 'w') as f:
          json.dump(sample_data, f)
     yield test_dir
     for f in os.listdir(test_dir):
          os.remove(os.path.join(test_dir, f))
     os.rmdir(test_dir)

def test_load_json_data_from_directory(test_dir):
     print('test is here 2')
     loader = DataLoader(test_dir)
     df = loader.load_json_data()
     assert isinstance(df, pd.DataFrame)
     assert len(df) == 1
     assert df.iloc[0]['id'] == "sample"

def test_load_json_data_from_list(test_dir):
     print('test is here 3')
     with open(os.path.join(test_dir, "sample.json"), 'r') as f:
          sample_data = json.load(f)
     data_list = [{"filename": "sample.json", "data": sample_data}]
     loader = DataLoader(data_list)
     df = loader.load_json_data()
     assert isinstance(df, pd.DataFrame)
     assert len(df) == 1
     assert df.iloc[0]['id'] == "sample"

def test_invalid_directory():
     print('test is here 4')
     with pytest.raises(ValueError):
          loader = DataLoader("invalid_directory")
          loader.load_json_data()

def test_invalid_list_input():
     print('test is here 5')
     with pytest.raises(ValueError):
          loader = DataLoader([{"invalid_key": "value"}])
          loader.load_json_data()