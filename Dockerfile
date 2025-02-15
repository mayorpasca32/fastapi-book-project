FROM python:3.11-slim  # Keeping the latest Python version

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt  # Keeping the cleaner pip install

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

