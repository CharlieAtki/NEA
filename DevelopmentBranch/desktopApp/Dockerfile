# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install dependencies (if you have any Python libraries to install)
RUN apt-get update && apt-get install -y \
    python3-tk \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . .

# Command to run your application
CMD ["python", "erp_hub.py"]
