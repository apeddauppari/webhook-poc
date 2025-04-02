# Use the official Python image as a base image
FROM python:3.9-slim

# Set the Current Working Directory inside the container
WORKDIR .

# Copy the requirements file if you have dependencies
RUN pip install flask

# Copy the source code into the container
COPY webhook-server.py .

# Copy TLS certificates
# COPY ./webhook.crt /certs/tls.crt
# COPY ./webhook.key /certs/tls.key
COPY server.pem /certs/tls.crt
COPY server-key.pem /certs/tls.key

# Expose port 443
EXPOSE 443

# Command to run the Python application
CMD ["python", "webhook-server.py"]