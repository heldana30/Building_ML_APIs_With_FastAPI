FROM python:3.10.9

# Set working directory
WORKDIR /app

# Copy requirements file
COPY ./src/backend/requirements.txt /app/

# Install dependencies
RUN python -m pip install --timeout 300000 --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY ./src/backend /app

# Copy the model files from dev/models
COPY ./dev/models /app/models

# Set environment variables for model paths
ENV XGBOOST_MODEL_PATH=/app/models/xgboost.joblib
ENV RANDOM_FOREST_MODEL_PATH=/app/models/random_forest.joblib
ENV ENCODER_PATH=/app/models/encoder.joblib

# Expose port
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]