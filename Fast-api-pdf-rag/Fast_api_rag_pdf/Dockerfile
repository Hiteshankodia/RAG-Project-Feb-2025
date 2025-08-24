# Use official Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install FastAPI and dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
