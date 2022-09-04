FROM python

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

# Commands to run Tkinter application
CMD ["./main_app.py"]
ENTRYPOINT ["python"]