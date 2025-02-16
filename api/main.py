from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import uvicorn
from .database import create_tables

# Debug: Print the Python path
# print("Python Path:", sys.path)

# Add the step_detection_data_science/src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../step_detection_data_science/src")))

# Use relative import for endpoints
from .endpoints.steps_prediction_json import router as json_router
from .endpoints.steps_prediction_db import router as db_router
from .endpoints.steps_crud_db import router as crud_router

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(json_router, prefix="/api")
app.include_router(db_router, prefix="/api")
app.include_router(crud_router, prefix="/api")

# Create database tables on startup
@app.on_event("startup")
async def startup():
    await create_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Step Prediction API \nList of API: http://127.0.0.1:8000/docs"}

# if __name__ == "__main__":
#     uvicorn.run("app", host="0.0.0.0", port=8000, reload=True)