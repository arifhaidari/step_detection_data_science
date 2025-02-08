import os

# Paths
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  
# RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "../raw_data")
MODEL_PATH = os.path.join(PROJECT_ROOT, "../models", "random_forest_model.pkl")
# JSON_FILE_PATH = os.path.join(PROJECT_ROOT, "../data", "calculated_steps.json")

# Constants
HEIGHT = -1.66
FS = 100.0  # Sampling frequency (Hz)
CUTOFF = 2.5  # Cutoff frequency (Hz)
ORDER = 4  # Filter order

# Paths and URLs
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  
MODEL_PATH = os.path.join(PROJECT_ROOT, "../models", "random_forest_model.pkl")

# PostgreSQL connection string
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/steps_db")

