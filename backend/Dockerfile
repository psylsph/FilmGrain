FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (pillow-heif usually has wheels, but for safety)
# git is required to install filmgrainer from source
RUN apt-get update && apt-get install -y libheif-dev git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Manually install filmgrainer
RUN git clone https://github.com/larspontoppidan/filmgrainer.git /tmp/filmgrainer \
    && cd /tmp/filmgrainer \
    && pip install . \
    && rm -rf /tmp/filmgrainer

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
