# Use Ubuntu 18.04 as the base image
FROM ubuntu:bionic

# Install necessary tools, libraries, and C dependencies
RUN apt update && apt install -y python3 python3-pip libffi-dev python3-dev

# Set the working directory in the container
WORKDIR /sawtooth-abac

# Copy the contents of the current directory into the container
COPY . .

# Install Python 3 specific dependencies
RUN python3 -m pip install --upgrade pip && python3 -m pip install lru-dict==1.2 marshmallow-annotations marshmallow~=3.2

# Make the log directory and Install the package using Python 3
RUN mkdir /var/log/sawtooth && python3 setup.py install
