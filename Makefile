PHONY: preview setup snapshot clear python clean

VENV_DIR = venv

preview:
	quarto preview --port 54321 --no-browser

setup:
	make clear
	make python
	make snapshot

	quarto add quarto-ext/shinylive --no-prompt

python:
	python -m venv venv
	pip install --upgrade pip
	pip install -r requirements.txt

snapshot:
	pip freeze > requirements_freeze.txt

clear:
	pip freeze | xargs pip uninstall -y
	make clean

clean:
	rm -rf _site .quarto _freeze

# Target to remove the existing virtual environment
clean_venv:
	rm -rf $(VENV_DIR)

# Target to create a new virtual environment and install requirements
venv: clean_venv
	python -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && pip install --upgrade pip
	$(MAKE) install_requirements

# Target to install dependencies from requirements.txt
install_requirements:
	. $(VENV_DIR)/bin/activate && pip install -r requirements.txt
