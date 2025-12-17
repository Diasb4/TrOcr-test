FROM python:3.10-slim

WORKDIR /app

# Установим системные зависимости
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы
COPY . /app

# Обновляем pip
RUN pip install --upgrade pip

# Устанавливаем пакеты по одному (так надежнее)
RUN pip install --no-cache-dir fastapi
RUN pip install --no-cache-dir uvicorn[standard]
RUN pip install --no-cache-dir python-multipart
RUN pip install --no-cache-dir pillow
RUN pip install --no-cache-dir pdf2image
RUN pip install --no-cache-dir paddlepaddle
RUN pip install --no-cache-dir paddleocr

# Создаём директории
RUN mkdir -p uploads train results

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]