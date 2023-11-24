# Use an official Python image as the base image
FROM python:3.10
MAINTAINER Wilson Zheng (wjz224@lehigh.edu)

# Create a directory for dependencies
RUN mkdir dependencies

# Copy the requirements file to the container
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --target=dependencies

# Add a command to zip the files
RUN apt-get update && apt-get install -y zip && rm -rf /var/lib/apt/lists/*

# Copy get_data.py for get_data_deploy_socrata
COPY ./AWS-Lambda-Ingestion/get_data_socrata.py dependencies/
COPY ./AWS-Lambda-Ingestion/get_data_non_socrata.py dependencies/
RUN cd dependencies && zip -r ../get_data_deploy .

# Set the working directory in the container
WORKDIR "/root"