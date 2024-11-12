FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

ENV FLASK_APP=Emmyapp.py
ENV FLASK_ENV=development

CMD ["python", "run", "--host=0.0.0.0", "--port=80"]
