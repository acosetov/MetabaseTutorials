FROM python:3.11

WORKDIR /app

COPY generate_data.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "generate_data.py"]