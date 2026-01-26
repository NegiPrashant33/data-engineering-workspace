# base Docker image that we will build on, slim python image
FROM python:3.12-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# set up the working directory inside the container
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages
# $PATH is an environment variable that tells the shell where to look for executable commands.
# below command puts the mentioned path in front of the of the list of directories where shell look for executable commands
# the command also activates the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (better layer caching)
COPY /pyproject.toml /.python-version /uv.lock /green_tripdata_2025-11.parquet /taxi_zone_lookup.csv ./

# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

# copy the script to the container. 1st name is source file, 2nd is destination
COPY 01-docker-data-pipeline/pipeline/homework_data_ingestion.py homework_data_ingestion.py

# define what to do first when the container runs
ENTRYPOINT ["python", "homework_data_ingestion.py"]