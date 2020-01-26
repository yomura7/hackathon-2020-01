.SILENT: run

run:
	apt-get -qqy update
	export DEBCONF_NOWARNINGS=yes
	apt-get -qqy install tesseract-ocr tesseract-ocr-jpn > /dev/null
	pip install -q pyocr pillow regex
	# python predict.py --image_dir data/test
	python predict_by_tesseract.py --mode ci
