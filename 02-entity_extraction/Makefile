.SILENT: run

run:
	apt-get -qqy update
	# export DEBCONF_NOWARNINGS=yes
	apt-get -qqy install tesseract-ocr > /dev/null
	# apt-get install -qqy tesseract-ocr-jpn
	# apt-get update && apt-get install -qqy tesseract-ocr libtesseract-dev
	pip install -q pyocr pillow
	python predict.py --image_dir data/test
