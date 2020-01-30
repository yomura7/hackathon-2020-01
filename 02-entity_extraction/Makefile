.SILENT: run

run:
	apt-get -qqy update
	export DEBCONF_NOWARNINGS=yes
	export LC_CTYPE="C.UTF-8"
	apt-get -qqy install python3-pip tesseract-ocr > /dev/null
	curl -sOL https://github.com/tesseract-ocr/tessdata_best/raw/master/jpn.traineddata
	mv jpn.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
	pip3 install -q pyocr pillow regex
	# python predict.py --image_dir data/test
	python3 predict_by_tesseract.py --mode ci
