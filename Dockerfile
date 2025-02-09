# Use an official Python image as a base
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

RUN pip install playwright && playwright install firefox --with-deps

# Copy the requirements file
COPY requirements.txt ./requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the application code
COPY ./src .

COPY ./profile_template ./profile_template

# Run the command to start the application
CMD ["python", "-u", "main.py"]