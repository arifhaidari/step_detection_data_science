import os
import json
import pandas as pd
import joblib
import numpy as np
import logging
from scipy.signal import find_peaks, butter, filtfilt

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

# Constants
HEIGHT = -1.66
fs = 100.0  # Sampling frequency (Hz)
cutoff = 2.5  # Cutoff frequency (Hz)
order = 4  # Filter order

# Paths
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "../data/data_raw")
MODEL_PATH = os.path.join(PROJECT_ROOT, "../models", "random_forest_model.pkl")
JSON_FILE_PATH = os.path.join(PROJECT_ROOT, "../data/data_output", "calculated_steps.json")

class DataLoader:
     def __init__(self, data_path):
          self.data_path = data_path
     
     def load_json_data(self):
          data_list = []
          files = [f for f in os.listdir(self.data_path) if f.endswith(".json")]
          for file in files:
               with open(os.path.join(self.data_path, file), 'r') as f:
                    data = json.load(f)
               df = pd.DataFrame(data)
               df['id'] = file.split('.')[0]
               df["time"] = pd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S.%f", errors='coerce')
               df["time"].fillna(pd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S", errors='coerce'), inplace=True)
               df['side'] = df['metadata'].apply(lambda x: x['side'])
               df.drop(columns=['metadata'], inplace=True)
               data_list.append(df)
          return pd.concat(data_list, ignore_index=True)

class DataPreprocessor:
     @staticmethod
     def butter_lowpass_filter(data, cutoff, fs, order=4):
          nyquist = 0.5 * fs
          normal_cutoff = cutoff / nyquist
          b, a = butter(order, normal_cutoff, btype='low', analog=False)
          return filtfilt(b, a, data)
     
     def preprocess(self, df):
          df["time"] = df["time"].fillna(method="ffill")
          df.set_index('time', inplace=True)
          df = df.sort_index()
          df['time_diff'] = df.index.to_series().diff().dt.total_seconds()
          sensor_columns = ["ax", "ay", "az", "gx", "gy", "gz"]
          for col in sensor_columns:
               df[col] = self.butter_lowpass_filter(df[col], cutoff, fs, order)
          return df

class FeatureExtractor:
     @staticmethod
     def extract_features(df):
          if df.get("time") is not None:
               df["time"] = pd.to_datetime(df["time"])
               df.set_index('time', inplace=True)
               df = df.sort_index()
          df.index = pd.to_datetime(df.index)
          session_features = df.groupby("id").agg({
               "ax": ["mean", "std", "min", "max"],
               "ay": ["mean", "std", "min", "max"],
               "az": ["mean", "std", "min", "max"],
               "gx": ["mean", "std", "min", "max"],
               "gy": ["mean", "std", "min", "max"],
               "gz": ["mean", "std", "min", "max"]
          }).reset_index()
          session_features.columns = ["_".join(col).strip() for col in session_features.columns.values]
          session_features = session_features.rename(columns={"id_": "id"})
          def count_peaks(series):
               peaks, _ = find_peaks(series, height=HEIGHT)
               return len(peaks)
          step_counts = df.groupby(["id", "side"])["az"].apply(count_peaks).unstack(fill_value=0)
          step_counts['left_steps'] = step_counts.get('L', 0)
          step_counts['right_steps'] = step_counts.get('R', 0)
          final_df = session_features.merge(step_counts, on="id")
          final_df['session_duration'] = (df.index.max() - df.index.min()).total_seconds()
          final_df['num_measurements'] = len(df)
          final_df['start_time'] = df.index.min()
          final_df['end_time'] = df.index.max()
          return final_df

class StepPredictor:
     def __init__(self, model_path):
          self.model = joblib.load(model_path)
     
     def predict(self, new_session_data):
          new_session_features = FeatureExtractor.extract_features(new_session_data)
          X_new = new_session_features.drop(columns=["id", "start_time", "end_time", "left_steps", "right_steps"])

          # Ensure consistency by dropping any extra columns
          expected_features = self.model.feature_names_in_  # Attributes available in sklearn models
          X_new = new_session_features.drop(columns=["id", "start_time", "end_time", "left_steps", "right_steps"], errors='ignore')

          # Keep only features that were present during training
          X_new = X_new[[col for col in X_new.columns if col in expected_features]]
          predicted_steps = self.model.predict(X_new)
          new_session_features["left_steps_pred"] = predicted_steps[:, 0].round().astype(int)
          new_session_features["right_steps_pred"] = predicted_steps[:, 1].round().astype(int)
          new_session_features["start_time"] = new_session_features["start_time"].dt.strftime("%Y-%m-%dT%H:%M:%S")
          new_session_features["end_time"] = new_session_features["end_time"].dt.strftime("%Y-%m-%dT%H:%M:%S")
          output = new_session_features[["id", "start_time", "end_time", "left_steps_pred", "right_steps_pred"]]
          return output.rename(columns={"left_steps_pred": "left_steps", "right_steps_pred": "right_steps"}).to_dict(orient="records")

class StepPredictionPipeline:
     def __init__(self, data_loader, preprocessor, predictor):
          self.data_loader = data_loader
          self.preprocessor = preprocessor
          self.predictor = predictor
     
     def run(self):
          df = self.data_loader.load_json_data()
          if df.empty:
               logging.error("No data found! Exiting.")
               return
          df = self.preprocessor.preprocess(df)
          unique_ids = df["id"].unique()
          all_predictions = []
          for unique_id in unique_ids:
               session_data = df[df["id"] == unique_id]
               predictions = self.predictor.predict(session_data)
               all_predictions.extend(predictions)
          with open(JSON_FILE_PATH, "w") as f:
               json.dump(all_predictions, f, indent=4)
          print("Predictions saved to calculated_steps.json")

if __name__ == "__main__":
     print('Processing - please wait ...')
     data_loader = DataLoader(RAW_DATA_PATH)
     preprocessor = DataPreprocessor()
     predictor = StepPredictor(MODEL_PATH)
     pipeline = StepPredictionPipeline(data_loader, preprocessor, predictor)
     pipeline.run()
     print("SUCCESS")
