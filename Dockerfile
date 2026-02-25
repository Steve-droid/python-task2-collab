FROM python:3.15.0a6-alpine3.23

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY templates/ /app/templates/

COPY app.py /app/

EXPOSE 5000

CMD ["python", "app.py"]
