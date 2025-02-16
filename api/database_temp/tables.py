from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Prediction(Base):
     __tablename__ = "predictions"

     id = Column(String, primary_key=True, index=True)  # Unique session ID
     start_time = Column(String)  # Start time of the session
     end_time = Column(String)  # End time of the session
     left_steps = Column(Integer)  # Predicted left steps
     right_steps = Column(Integer)  # Predicted right steps
     timestamp = Column(DateTime, default=datetime.utcnow)  # Timestamp of the prediction