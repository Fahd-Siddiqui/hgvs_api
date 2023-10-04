# Makefile

# Commands
.PHONY: lint test docker requirements requirements-test install prepare deploy

# Lint: Checks flake8, mypy, isort
lint:
	@echo "Running isort..."
	@isort --check-only .
	@echo "Running lint..."
	@black src
	@flake8 src --exclude=venv* --max-line-length=120
	@echo "Running mypy..."
	@mypy src

# Tests: pytest from src folder with coverage and printing coverage report
test:
	@echo "Running tests with coverage..."
	@coverage run -m pytest test
	@coverage report

# Requirements: installs test requirements
requirements-test:
	@echo "Installing test requirements"
	@pip install -r requirements_test.txt

# Requirements: installs requirements
requirements:
	@echo "Installing requirements"
	@pip install -r requirements.txt

# Deploy: Builds docker image
docker:
	@echo "Building docker image..."
	@docker compose build
	@echo "Run docker compose up -d"

# Prepare venv
prepare:
	@echo "Preparing venv..."
	@python -m venv venv
	@source venv/bin/activate

install: prepare requirements

deploy: install requirements_test test docker