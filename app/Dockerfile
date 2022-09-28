FROM python:3.8-slim-buster

#Deault workdir
WORKDIR /app

# Download Package Information
RUN apt-get update -y
# Install Tkinter
RUN apt-get install python3-opencv -y

# Copy file with requierements to install 
COPY requirements.txt requirements.txt

# Add the files to folder app
ADD . /app

# Update pip
RUN pip3 install --upgrade pip

# Install requirements
RUN pip3 install -r requirements.txt

ADD https://github.com/afrincon/neumonia_detector/releases/download/model/WilhemNet_86.h5 /app/backend/

# Commands to run Tkinter application
CMD ["./main_app.py"]
ENTRYPOINT ["python"]