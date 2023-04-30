# Use the official Python 3 slim base image
FROM python:3-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY . .

# Expose the port the app will run on
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
