# Use a lightweight Python image
FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set the default command to run the application
CMD ["python", "app.py"]
