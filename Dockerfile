# Use official Python 12 slim image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# default db location 
ENV DB_URL="/mnt/md.db"
ENV REDIS_HOST=redis-server

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# server 
EXPOSE 3000

# Default command
CMD ["python3", "main.py"]