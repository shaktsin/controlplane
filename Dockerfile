# Use official Python 12 slim image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# default db location 
ENV DB_URL="/mnt/md.db"

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python3", "main.py"]