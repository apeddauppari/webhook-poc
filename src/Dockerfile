# Use the official Python image as a base image
FROM python:3.9-slim

# Set the Current Working Directory inside the container
WORKDIR .

# Copy the requirements file if you have dependencies
RUN pip install flask

# Copy the source code into the container
COPY webhook-server.py .

# Copy TLS certificates
COPY tls.crt /certs/tls.crt
COPY tls.key /certs/tls.key

EXPOSE 8080

# Command to run the Python application
CMD ["python", "webhook-server.py"]