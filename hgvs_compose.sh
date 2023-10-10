#!/bin/bash

# Set the name for your containers
SEQREPO_CONTAINER="seqrepo_rsync"
UTA_DB_CONTAINER="uta_db"
API_CONTAINER="api"

# Function to check if volumes exist
check_volumes_exist() {
  if ! docker volume inspect seqrepo_data &>/dev/null || ! docker volume inspect uta_db_data &>/dev/null; then
    echo "Docker volumes seqrepo_data and uta_db_data do not exist. Creating them..."
    docker volume create seqrepo_data
    docker volume create uta_db_data
  fi
}

# Function to build Docker images
build_images() {
  # Build the seqrepo_rsync image from the seqrepo directory
  docker build -t hgvs-seqrepo_rsync ./seqrepo

  # Build the uta_db image from the uta directory (replace with the actual build command)
  docker build -t hgvs-uta_db ./uta

  # Build the API image from the current directory (replace with the actual build command)
  docker build -t hgvs-api .
}

# Function to start containers
start_containers() {
  check_volumes_exist

  # Start the seqrepo_rsync container
  docker run -d --name $SEQREPO_CONTAINER \
    -v seqrepo_data:/seqrepo \
    hgvs-seqrepo_rsync

  # Wait for the seqrepo_rsync container to complete its task (you may need to customize this)
  docker wait $SEQREPO_CONTAINER

  # Start the uta_db container
  docker run -d --name $UTA_DB_CONTAINER \
    -p 5432:5432 \
    -v uta_db_data:/var/lib/postgresql/data \
    hgvs-uta_db

  # Start the API container
  docker run -d --name $API_CONTAINER \
    -p 8000:8000 \
    -v seqrepo_data:/seqrepo \
    -e UTA_DB_URL=postgresql://anonymous@${UTA_DB_CONTAINER}:5432/uta/uta_20210129 \
    -e HGVS_SEQREPO_DIR=/seqrepo/latest \
    -e GRANT_SUDO=yes \
    -e WEB_CONCURRENCY=16 \
    hgvs-api

  # Optionally, you can add more commands here, such as running database migrations or other setup tasks.
}

# Function to stop containers
stop_containers() {
  docker stop $SEQREPO_CONTAINER $UTA_DB_CONTAINER $API_CONTAINER
  docker rm $SEQREPO_CONTAINER $UTA_DB_CONTAINER $API_CONTAINER
}

# Function to display help menu
show_help() {
  echo "Usage: $0 {start|stop|build|help}"
  echo "  start  - Start containers"
  echo "  stop   - Stop containers"
  echo "  build  - Build Docker images"
  echo "  help   - Show this help message"
}

# Check for command-line arguments
case "$1" in
  start)
    start_containers
    ;;
  stop)
    stop_containers
    ;;
  build)
    build_images
    ;;
  help)
    show_help
    ;;
  *)
    show_help
    exit 1
esac

exit 0
