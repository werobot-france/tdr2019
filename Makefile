.SILENT:
.PHONY: arduino

arduino:
	arduino-cli compile --fqbn arduino:avr:uno ./arduino && arduino-cli upload --fqbn arduino:avr:uno -p /dev/ttyACM0 ./arduino
python:
	python3 __main__.py
install:
	pip3 install -r requirements.txt && npm install

