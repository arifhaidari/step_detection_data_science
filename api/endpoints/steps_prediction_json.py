from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import json
# import pandas as pd
from datetime import datetime
import sys
from typing import List

# Add the step_detection_data_science/src directory to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../step_detection_data_science/src")))

# Import the classes from src directory 
# from data_loader import DataLoader 
# from data_processor import DataPreprocessor
# from steps_predictor import StepPredictionPipeline, StepPredictor

from src.data_loader import DataLoader
from src.data_processor import DataPreprocessor
from src.steps_predictor import StepPredictionPipeline, StepPredictor

# import schema
from ..schema.prediction_schema import PredictionResponse

router = APIRouter()

# Constants (without using docker container)
# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# MODEL_PATH = os.path.join(PROJECT_ROOT, "../../../step_detection_data_science/models", "random_forest_model.pkl")
# OUTPUT_DIR = os.path.join(PROJECT_ROOT, "../../../step_detection_data_science/data/data_output")


# using docker container 
PROJECT_ROOT = "/app"

# Define MODEL_PATH relative to PROJECT_ROOT
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "random_forest_model.pkl")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data/data_output")

# Ensure output directory exists
# os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/predict-json", response_model=List[PredictionResponse])
async def predict_steps_json(
     summary="Predict step counts",
     files: list[UploadFile] = File(...)
     ):
     """
     Predicts the number of steps based on sensor data and store them in JSON file.

     - **files**: A list of JSON files containing sensor data.

     Returns:
     - A list of predictions with step counts.
     """
     try:
          # Read uploaded files into memory
          uploaded_files = []
          for file in files:
               if not file.filename.endswith(".json"):
                    raise HTTPException(status_code=400, detail="Only .json files are allowed")
               
               # Read the file content
               content = await file.read()
               data = json.loads(content)
               uploaded_files.append({
                    "filename": file.filename,
                    "data": data
               })

          # Pass the list of file content to DataLoader
          data_loader = DataLoader(uploaded_files)
          preprocessor = DataPreprocessor()
          predictor = StepPredictor(MODEL_PATH)
          pipeline = StepPredictionPipeline(data_loader, preprocessor, predictor)

          # Run the pipeline
          predictions = pipeline.run()

          # Save predictions to a unique JSON file
          timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
          output_file = os.path.join(OUTPUT_DIR, f"predictions_{timestamp}.json")
          with open(output_file, "w") as f:
               json.dump(predictions, f, indent=4)

          # Read the saved predictions and return them
          with open(output_file, "r") as f:
               prediction_results = json.load(f)

          return predictions
     except Exception as e:
          raise HTTPException(status_code=500, detail=str(e))