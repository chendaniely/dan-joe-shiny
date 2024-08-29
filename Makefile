PHONY: preview setup snapshot clear python clean

preview:
	quarto preview --port 54321 --no-browser

setup:
	make clear
	make python
	make snapshot

	quarto add quarto-ext/shinylive --no-prompt

python:
	pip install --upgrade pip
	pip install -r requirements.txt

snapshot:
	pip freeze > requirements_freeze.txt

clear:
	pip freeze | xargs pip uninstall -y
	make clean

clean:
	rm -rf _site .quarto _freeze
