APP_DIR = app
VENV_DIR = .venv

ifeq ($(OS),Windows_NT)
    VENV_BIN = $(APP_DIR)/$(VENV_DIR)/Scripts
    PYTHON = $(VENV_BIN)/python.exe
    PIP = $(VENV_BIN)/pip.exe
else
    VENV_BIN = $(APP_DIR)/$(VENV_DIR)/bin
    PYTHON = $(VENV_BIN)/python
    PIP = $(VENV_BIN)/pip
endif

docker-db-run:
	cd $(APP_DIR) && docker-compose up --build -d
	@echo "Docker database created."

venv:
	python -m venv $(APP_DIR)/$(VENV_DIR)
	@echo "Virtual environment created."

install: venv
	$(PIP) install -r $(APP_DIR)/requirements.txt
	@echo "Dependencies installed."

run: install docker-db-run
	$(PYTHON) -m $(APP_DIR).main

clean:
	rm -rf $(APP_DIR)/$(VENV_DIR)
	@echo "Cleaned up the virtual environment."

all: run
	@echo "Project setup."

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  docker-db-run	 Create database in Docker"
	@echo "  venv      Create virtual environment"
	@echo "  install	 Install dependencies"
	@echo "  clean     Clean the environment"
	@echo "  run       Set up the project (venv + Docker database)"
	@echo "  all       Run the full pipeline (setup, Docker)"