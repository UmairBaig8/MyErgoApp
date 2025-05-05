# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and assets into the container at /app
COPY main.py .
COPY assets/ /app/assets/

# Make port 8550 available to the world outside this container
EXPOSE 8550

# Define environment variable (optional, Flet default is 8550)
# ENV PORT 8550

# Run main.py as a web app when the container launches
# -w runs in web mode
# -p specifies the port
CMD ["flet", "run", "main.py", "-w", "-p", "8550"]
