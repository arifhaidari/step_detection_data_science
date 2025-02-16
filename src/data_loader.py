import os
import json
import pandas as pd

# ignore warnings
import warnings
warnings.filterwarnings("ignore")


class DataLoader:
     def __init__(self, input_data):
          """
          Initialize the DataLoader.

          Args:
               input_data: Can be either a directory path (str) or a list of dictionaries containing file content.
                         Each dictionary should have:
                         - "filename": The name of the file.
                         - "data": The JSON content of the file.
          """
          self.input_data = input_data

     def load_json_data(self):
          """
          Load and process JSON data.

          Returns:
               pd.DataFrame: A concatenated DataFrame containing data from all files.
          """
          data_list = []

          if isinstance(self.input_data, str):
               # Input is a directory path
               if not os.path.isdir(self.input_data):
                    raise ValueError(f"The provided path '{self.input_data}' is not a valid directory.")

               files = [f for f in os.listdir(self.input_data) if f.endswith(".json")]
               for file in files:
                    file_path = os.path.join(self.input_data, file)
                    with open(file_path, 'r') as f:
                         data = json.load(f)
                    df = self._process_file(data, file)
                    data_list.append(df)
          elif isinstance(self.input_data, list):
               # Input is a list of file content
               for file in self.input_data:
                    if not isinstance(file, dict) or "filename" not in file or "data" not in file:
                         raise ValueError("Each item in the list must be a dictionary with 'filename' and 'data' keys.")
                    df = self._process_file(file["data"], file["filename"])
                    data_list.append(df)
          else:
               raise ValueError("Input must be either a directory path (str) or a list of file content.")

          return pd.concat(data_list, ignore_index=True)

     def _process_file(self, data, filename):
          """
          Process a single JSON file and return a DataFrame.

          Args:
               data: The JSON content of the file.
               filename: The name of the file.

          Returns:
               pd.DataFrame: A DataFrame containing the processed data.
          """
          df = pd.DataFrame(data)
          df['id'] = filename.split('.')[0]  # Use the filename as the ID
          df["time"] = pd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S.%f", errors='coerce')
          df["time"].fillna(pd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S", errors='coerce'), inplace=True)
          df['side'] = df['metadata'].apply(lambda x: x['side'])
          df.drop(columns=['metadata'], inplace=True)
          return df