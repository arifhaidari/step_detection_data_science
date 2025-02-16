from fastapi import APIRouter, Depends, HTTPException, Path
from databases import Database
from sqlalchemy import select, delete
from typing import List

# import database methods
from ..database import predictions_table, database, get_db

# import schema
from ..schema.prediction_schema import PredictionList

router = APIRouter()

@router.get("/predictions", response_model=List[PredictionList])
async def list_predictions(db: Database = Depends(get_db)):
     """
     List all predictions stored in the database.

     Returns:
     - A list of predictions with step counts and timestamps.
     """
     try:
          # Query to fetch all predictions
          query = select(predictions_table)
          predictions = await db.fetch_all(query)

          # Return the predictions
          return predictions
     except Exception as e:
          raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictions/detail/{prediction_id}", response_model=PredictionList)
async def get_prediction_by_id(
     prediction_id: str = Path(..., description="The ID of the prediction to retrieve."),
     db: Database = Depends(get_db)
     ):
     """
     Retrieve the details of a specific prediction by its ID.

     Parameters:
     - **prediction_id**: The unique ID of the prediction to retrieve.

     Returns:
     - The prediction details.
     """
     try:
          # Query to fetch the prediction by ID
          query = select(predictions_table).where(predictions_table.c.id == prediction_id)
          prediction = await db.fetch_one(query)

          # Check if the prediction exists
          if prediction:
               return prediction
          else:
               raise HTTPException(status_code=404, detail=f"Prediction with ID {prediction_id} not found.")
     except Exception as e:
          raise HTTPException(status_code=500, detail=str(e))
     

@router.delete("/predictions/{prediction_id}", response_model=dict)
async def delete_prediction(
     prediction_id: str = Path(..., description="The ID of the prediction to delete."),
     db: Database = Depends(get_db)
     ):
     """
     Delete a prediction by its ID.

     Parameters:
     - **prediction_id**: The unique ID of the prediction to delete.

     Returns:
     - A confirmation message.
     """
     try:
          # Query to delete the prediction by ID
          query = delete(predictions_table).where(predictions_table.c.id == prediction_id)
          await db.execute(query) 

          return {"message": f"Prediction deleted successfully."}
          # else:
          #      raise HTTPException(status_code=404, detail=f"Prediction with ID {prediction_id} not found.")
     except Exception as e:
          raise HTTPException(status_code=500, detail=str(e))