FROM python:3.10-slim

WORKDIR /app

# OpenCV ve pyzbar (QR okuyucu) için sistem seviyesindeki gerekli C++ ve Linux kütüphaneleri
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY backend/ ./backend/
COPY imwatermark/ ./imwatermark/
# Örnek görsel
COPY cover_image.png . 

# FastAPI sunucusunu ayağa kaldır
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
