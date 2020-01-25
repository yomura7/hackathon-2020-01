.SILENT: run

run:
	export DEBCONF_NOWARNINGS=yes
	apt-get -qqy update
	apt-get install -qqy tesseract-ocr
	# apt-get install -qqy tesseract-ocr-jpn
	# apt-get update && apt-get install -qqy tesseract-ocr libtesseract-dev
	pip install -q pyocr pillow
	python predict.py --image_dir data/test
