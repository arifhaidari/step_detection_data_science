from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PredictionResponse(BaseModel):
     id: str
     start_time: str
     end_time: str
     left_steps: int
     right_steps: int
     num_measurements: int
     session_duration: float

# this schema inherit all attributes from PredictionResponse and add timestamp to it 
class PredictionList(PredictionResponse):
    timestamp: datetime  # Pydantic will automatically serialize datetime to JSON
    
    model_config = ConfigDict(from_attributes=True)