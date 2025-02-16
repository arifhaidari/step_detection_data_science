import os

class Settings:
     PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
     RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "../../data/data_raw")
     MODEL_PATH = os.path.join(PROJECT_ROOT, "../../models", "random_forest_model.pkl")
     # JSON_FILE_PATH = os.path.join(PROJECT_ROOT, "../../data/data_output", "calculated_steps.json")

settings = Settings()