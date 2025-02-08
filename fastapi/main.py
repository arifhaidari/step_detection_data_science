from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from .config import DATABASE_URL
from .model import load_model, predict_steps
from .data_processing import load_json_data, preprocess_data
from .models import SessionLocal, StepPrediction
import json

app = FastAPI()

# Load model once at startup
model = load_model(MODEL_PATH)

def get_db():
     db = SessionLocal()
     try:
          yield db
     finally:
          db.close()

@app.post("/calculate_steps")
def calculate_steps_for_multiple_sessions(db: Session = Depends(get_db)):
     df = load_json_data()  # Assume that data is uploaded via API
     df = preprocess_data(df)

     predictions = predict_steps(df, model)
     
     # Insert predictions into the PostgreSQL database
     for prediction in predictions:
          db.add(StepPrediction(**prediction))
     db.commit()

     return {"message": "Step counts calculated and saved to database."}
