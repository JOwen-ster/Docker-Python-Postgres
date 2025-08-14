# 1. Use an official Python runtime as a parent image
FROM python:3.12-slim

# 2. Set the working directory in the container
WORKDIR /usr/src/bot

# 3. Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application code
COPY . .

# 5. Command to run the application
CMD ["python", "-u", "app.py"]