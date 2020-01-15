.SILENT: run

run:
	apt-get install -qqy tesseract-ocr libtesseract-dev
	pip install -q pyocr pillow pandas
	python predict.py --image_dir data/test
