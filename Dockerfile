# Use an official Python image as a base
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install firefox

# Copy the application code
COPY ./src .

# Run the command to start the application
CMD ["python", "-u", "main.py"]