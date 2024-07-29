FROM python:3.10.9

# Set working directory
WORKDIR /app

# Copy requirements file
COPY ./src/frontend/requirements.txt /app/

# Install dependencies
RUN python -m pip install --timeout 300000 --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY ./src/frontend /app

# Expose port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "predict.py", "--server.port", "8501", "--server.address", "0.0.0.0"]