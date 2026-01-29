FROM python:3.10-slim

# Install system dependencies and gcsfuse
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    tini \
    && export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s` \
    && echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | tee /etc/apt/sources.list.d/gcsfuse.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && apt-get update \
    && apt-get install -y gcsfuse \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY scripts ./scripts

# Ensure entrypoint is executable
RUN chmod +x ./scripts/entrypoint.sh

# Default environment variables
ENV PORT=8080
ENV MOUNT_POINT=/mnt/gcs

# Use tini to manage processes and signal propagation
ENTRYPOINT ["/usr/bin/tini", "--"]

# Run the entrypoint script
CMD ["./scripts/entrypoint.sh"]
