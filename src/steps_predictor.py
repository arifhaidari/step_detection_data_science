import os
import json
import numpy as np
import joblib
import logging
from datetime import datetime
import sys

# Debug: Print the Python path
# print("Python Path:", sys.path)


# ignore warnings
import warnings
warnings.filterwarnings("ignore")


# Paths
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "../data/data_raw")
MODEL_PATH = os.path.join(PROJECT_ROOT, "../models", "random_forest_model.pkl")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "../data/data_output")

# to get the current absolute address for importing data_loader, data_processor
sys.path.append(os.path.join(PROJECT_ROOT))


# import my custom classes
from data_loader import DataLoader
from data_processor import DataPreprocessor, FeatureExtractor


class StepPredictor:
     def __init__(self, model_path):
          self.model = joblib.load(model_path)
     
     def predict(self, new_session_data):
          new_session_features = FeatureExtractor.extract_features(new_session_data)
          
          X_new = new_session_features.copy()

          # Ensure consistency by dropping any extra columns
          expected_features = self.model.feature_names_in_  # Attributes available in sklearn models

          # Keep only features that were present during training
          X_new = X_new[[col for col in new_session_features.columns if col in expected_features]]
          predicted_steps = self.model.predict(X_new)
          
          new_session_features["left_steps"] = predicted_steps[:, 0].round().astype(int)
          new_session_features["right_steps"] = predicted_steps[:, 1].round().astype(int)
          
          output = new_session_features[["id", "start_time", "end_time", "left_steps", "right_steps", "session_duration", "num_measurements"]]
          
          # Convert Timestamp columns to ISO format strings
          output['start_time'] = output['start_time'].apply(lambda x: x.isoformat())
          output['end_time'] = output['end_time'].apply(lambda x: x.isoformat())
          
          return output.to_dict(orient="records")

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
          return all_predictions

if __name__ == "__main__":
     print('Processing - please wait ...')
     data_loader = DataLoader(RAW_DATA_PATH)
     preprocessor = DataPreprocessor()
     predictor = StepPredictor(MODEL_PATH)
     pipeline = StepPredictionPipeline(data_loader, preprocessor, predictor)
     prediction_result = pipeline.run()
     
     # Save predictions to a unique JSON file
     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
     output_file = os.path.join(OUTPUT_DIR, f"predictions_{timestamp}.json")
     with open(output_file, "w") as f:
          json.dump(prediction_result, f, indent=4)
          
     print("SUCCESS")
