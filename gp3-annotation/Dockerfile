# Using latest Python image
FROM python:latest

# My credentials
LABEL maintainer="morgan.nolan@hotmail.com"

# Copying folder contents
COPY ["/gp3-annotation", ".env", "/gp3-annotation/"]

# Setting our working directory
WORKDIR /gp3-annotation

# Installing required Python libraries
RUN pip install -r requirements.txt

# Running server.py when container is started
CMD ["python", "-u", "gp3-annotation.py"]