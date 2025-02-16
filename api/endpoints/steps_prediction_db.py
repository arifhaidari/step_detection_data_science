from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
import json
from datetime import datetime
import sys
from databases import Database
from sqlalchemy import select
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

# import database methods
from ..database import predictions_table, database, get_db

# import schema
from ..schema.prediction_schema import PredictionResponse

router = APIRouter()

# Constants (without docker container)
# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# MODEL_PATH = os.path.join(PROJECT_ROOT, "../../../step_detection_data_science/models", "random_forest_model.pkl")
# Define PROJECT_ROOT relative to the container's working directory

# using docker container 
PROJECT_ROOT = "/app"

# Define MODEL_PATH relative to PROJECT_ROOT
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "random_forest_model.pkl")

@router.post("/predict-db", response_model=List[PredictionResponse])
async def predict_steps_db(
          summary="Predict step counts",
          files: list[UploadFile] = File(...),
          db: Database = Depends(get_db)
     ):
     """
     Predicts the number of steps based on sensor data and store them in database.

     - **files**: A list of JSON files containing sensor data.
     - **db**: A database connection dependency.

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

          # Save predictions to the database
          for prediction in predictions:
               # Check if the ID already exists in the database
               query = select(predictions_table).where(predictions_table.c.id == prediction["id"])
               existing_record = await db.fetch_one(query)
               if existing_record:
                    continue  # Skip if the ID already exists
                    # raise HTTPException(status_code=400, detail=f"Record with id {prediction['id']} already exists")

               # Add a timestamp to the prediction
               # datetime.now().isoformat(): Convert datetime to string before inserting into the database
               prediction["timestamp"] = datetime.now()

               # Insert the prediction into the database
               insert_query = predictions_table.insert().values(**prediction)
               await db.execute(insert_query)
          return predictions
     except Exception as e:
          raise HTTPException(status_code=500, detail=str(e))