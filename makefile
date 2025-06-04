APP_DIR = app
VENV_DIR = .venv

docker-db-run:
	cd $(APP_DIR) && docker-compose up --build -d
	cd ..
	@echo "Docker database created."

venv:
	python -m venv $(APP_DIR)/$(VENV_DIR)
	@echo "Virtual environment created."

activate-venv: venv
	$(APP_DIR)/$(VENV_DIR)/scripts/activate
	@echo ".venv activated."

install: activate-venv
	$(APP_DIR)/$(VENV_DIR)/bin/pip install -r $(APP_DIR)/requirements.txt
	@echo "Dependencies installed."

run: activate-venv docker-db-run
	python -m $(APP_DIR).src.main

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
	@echo "  activate-venv	 Activate venv"
	@echo "  install	 Install dependencies"
	@echo "  clean     Clean the environment"
	@echo "  run       Set up the project (venv + Docker database)"
	@echo "  all       Run the full pipeline (setup, Docker)"