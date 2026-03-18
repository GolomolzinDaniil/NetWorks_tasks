FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libgbm1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install msedge
RUN playwright install-deps

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]