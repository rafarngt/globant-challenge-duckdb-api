FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY api/ ./

# Copy data folder from root context
COPY data/ ./data/

# Create necessary directories for DuckDB
RUN mkdir -p ./data/duckdb/db

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8081 for local development
EXPOSE 8081

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :${PORT:-8081} --workers 1 --threads 8 --timeout 0 app:app
