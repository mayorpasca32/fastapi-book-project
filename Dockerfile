<<<<<<< HEAD
FROM python:3.11-slim
=======
FROM python:3.8-slim
>>>>>>> 9ccfdb9d855c7153a8bd5c164e357270847542fe

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
<<<<<<< HEAD
    pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

=======
    pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 9ccfdb9d855c7153a8bd5c164e357270847542fe
