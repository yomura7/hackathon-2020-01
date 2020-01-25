.SILENT: run

run:
	# echo "deb https://notesalexp.org/tesseract-ocr/buster/ buster main" >> /etc/apt/sources.list
	# apt-get update -oAcquire::AllowInsecureRepositories=true
	# apt-get install notesalexp-keyring -oAcquire::AllowInsecureRepositories=true
	apt-get update
	apt-get install tesseract-ocr
	# apt-get install tesseract-ocr-jpn
	# apt-get update && apt-get install -qqy tesseract-ocr libtesseract-dev
	pip install -q pyocr pillow
	python predict.py --image_dir data/test
