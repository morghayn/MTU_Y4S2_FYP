# Using latest Python image
FROM python:latest

# My credentials
LABEL maintainer="morgan.nolan@hotmail.com"

# Copying folder contents
COPY ["/retriever", ".env", "/retriever/"]

# Setting our working directory
WORKDIR /retriever

# Installing required Python libraries
RUN pip install -r requirements.txt

# Running server.py when container is started
CMD ["python", "-u", "retriever.py"]