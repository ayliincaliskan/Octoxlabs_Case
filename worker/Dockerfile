# Python imajını seçin
FROM python:3.9-slim

# Çalışma dizinini ayarlayın
WORKDIR /app

# Gereksinimleri kopyalayın ve yükleyin
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyalayın
COPY . .

# Worker'ı başlatacak komutu belirtin
CMD ["python", "worker.py"]