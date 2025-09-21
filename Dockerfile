FROM python:3.13-slim
LABEL authors="arthur"
WORKDIR /app
COPY shared_models/ ./shared_models/
COPY gateway-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY gateway-service/main.py .
EXPOSE 8000
CMD ["python", "main.py"]