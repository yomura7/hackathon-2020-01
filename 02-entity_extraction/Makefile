.SILENT: run

run:
	apt-get -qqy update
	export DEBCONF_NOWARNINGS=yes
	export LC_CTYPE="C.UTF-8"
	apt-get -qqy install python3-pip tesseract-ocr tesseract-ocr-jpn > /dev/null
	pip3 install -q pyocr pillow regex opencv-python
	# python predict.py --image_dir data/test
	python3 predict_by_tesseract.py --mode ci
