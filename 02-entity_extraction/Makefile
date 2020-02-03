.SILENT: run

run:
	apt-get -qqy update
	export DEBCONF_NOWARNINGS=yes
	export LC_CTYPE="C.UTF-8"
	apt-get -qqy install python3-pip tesseract-ocr > /dev/null
 	curl -sOL https://github.com/yomura7/hackathon-2020-01/blob/tuningocr/02-entity_extraction/resource/kanji_10000.traineddata
 	mv -f kanji_10000.traineddata /usr/share/tesseract-ocr/4.00/tessdata/jpn.traineddata
	pip3 install -q pyocr pillow regex
	# python predict.py --image_dir data/test
	python3 predict_by_tesseract.py --mode ci
