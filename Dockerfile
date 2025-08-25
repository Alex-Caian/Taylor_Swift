# Use an official lightweight Python image
FROM python:3.11-slim

# Create a working directory
WORKDIR /app

# Install dependencies early (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port for Cloud Run
ENV PORT=8080

# Start your app (replace with your actual entry point if different)
CMD ["python", "app.py"]
