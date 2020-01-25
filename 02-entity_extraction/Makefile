run:
	apt-get update
	apt-get install -qqy tesseract-ocr
	dpkg -l | grep "tesseract"
	# apt-get install -qqy tesseract-ocr-jpn
	# apt-get update && apt-get install -qqy tesseract-ocr libtesseract-dev
	pip install -q pyocr pillow
	python predict.py --image_dir data/test
