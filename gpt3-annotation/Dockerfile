# Using latest Python image
FROM python:latest

# My credentials
LABEL maintainer="morgan.nolan@hotmail.com"

# Copying folder contents
COPY ["/gpt3-annotation", ".env", "/gpt3-annotation/"]

# Setting our working directory
WORKDIR /gpt3-annotation

# Installing required Python libraries
RUN pip install -r requirements.txt

# Running server.py when container is started
CMD ["python", "-u", "gpt3-annotation.py"]