# Using latest Python image
FROM python:latest

# My credentials
LABEL maintainer="morgan.nolan@hotmail.com"

# Copying folder contents
COPY ["/annotator", ".env", "/annotator/"]

# Setting our working directory
WORKDIR /annotator

# Installing required Python libraries
RUN pip install -r requirements.txt

# Exposing port
EXPOSE 8080

# Running app.py when container is tarted
CMD ["python", "app.py"]