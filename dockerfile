# Use a lightweight Python image
FROM python:latest

WORKDIR /devops_projekt

COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the application code
COPY devops_projekt/ .

# Set the default command to run the application
CMD ["python", "app.py"]
