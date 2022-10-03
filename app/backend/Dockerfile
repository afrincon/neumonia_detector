FROM python:3.8-slim-buster

WORKDIR /app

# update and install packages
RUN apt-get update \
  && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential

# Install Tkinter
RUN apt-get install python3-opencv -y

# Copy file with requierements to install 
COPY app/backend/requirements.txt requirements.txt

# Update pip
RUN pip3 install --upgrade pip

# Install requirements
RUN pip3 install -r requirements.txt

# Add the files to folder app
COPY app/backend/src .

# Add proto files
COPY protos/backend.proto .

# run protos
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./backend.proto