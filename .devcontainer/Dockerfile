FROM python:3.7.3

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    apt-utils \
    gcc \
    build-essential \
    tesseract-ocr \
    tesseract-ocr-jpn \
    && pip install --no-cache-dir \
    autopep8 \
    flake8 \
    pyocr \
    pillow \
    regex \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
    