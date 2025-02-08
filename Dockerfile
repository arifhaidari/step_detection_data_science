# official Python runtime as a parent image
FROM python:3.10-slim

# working directory in the container
WORKDIR /app

COPY fastapi /app
COPY models /app

# Install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
