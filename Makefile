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
docker-build:
	@echo "Building docker image..."
	@docker compose build
	@echo "Run docker compose up -d"

# Saves the docker images
docker-save: docker-build
	@echo "Saving images to output/"
	@mkdir -p output
	@docker save hgvs-api |gzip > output/hgvs-api-docker.tar.gz
	@docker save hgvs-seqrepo_rsync |gzip > output/hgvs-seqrepo_rsync-docker.tar.gz
	@docker save hgvs-uta_db |gzip > output/hgvs-uta_db-docker.tar.gz

# Loads the docker images
docker-load:
	@echo "Loading images from output/"
	@gunzip -c output/hgvs-api-docker.tar.gz | docker load
	@gunzip -c output/hgvs-seqrepo_rsync-docker.tar.gz | docker load
	@gunzip -c output/hgvs-uta_db-docker.tar.gz | docker load


# Prepare venv
prepare:
	@echo "Preparing venv..."
	@python -m venv venv
	@source venv/bin/activate

install: prepare requirements

deploy: install requirements_test test docker-build