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
	pip install prompt-toolkit==3.0.36 ipython==7.34.0 shiny ipykernel shinylive
	pip install pandas pyyaml jupyter seaborn

snapshot:
	pip freeze > requirements.txt

clear:
	pip freeze | xargs pip uninstall -y
	make clean

clean:
	rm -rf _site .quarto
