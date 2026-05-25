FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/engine/ ./src/engine/
COPY config/ ./config/

EXPOSE 8000

CMD ["python", "src/engine/main.py"]
