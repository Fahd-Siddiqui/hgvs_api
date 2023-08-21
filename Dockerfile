# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

RUN apt update
RUN apt install -y build-essential postgresql libpq-dev

# Install the required dependencies
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

# Copy the application files into the container
COPY ./src /app/src

# Expose the port the FastAPI app will run on
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "src.hgvs_api:app", "--host", "0.0.0.0", "--port", "8000"]
