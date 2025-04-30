FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl chromium-driver chromium \
    && apt-get clean

ENV CHROME_BIN=/usr/bin/chromium

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]