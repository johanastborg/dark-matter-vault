#!/bin/bash
set -e

# Define mount point and bucket name
MNT_DIR=${MOUNT_POINT:-/mnt/gcs}
BUCKET=${BUCKET_NAME}

echo "Starting Cloud Run Service..."

if [ -z "${BUCKET}" ]; then
    echo "BUCKET_NAME not set, skipping gcsfuse mount."
else
    echo "Checking mount point: ${MNT_DIR}"
    mkdir -p ${MNT_DIR}

    # Check if already mounted (e.g. via Cloud Run Volume Mounts)
    if grep -qs "${MNT_DIR} " /proc/mounts; then
        echo "Volume already mounted at ${MNT_DIR}"
    else
        echo "Mounting GCS Bucket: ${BUCKET} to ${MNT_DIR} using gcsfuse..."
        # Run gcsfuse in background or foreground?
        # If we run in background, we need to make sure it stays running.
        # But gunicorn is our main process.
        # Using implicit-dirs to see "folders" in GCS
        gcsfuse --debug_gcs --debug_fuse --implicit-dirs ${BUCKET} ${MNT_DIR}
        echo "Mounting command executed."
    fi
fi

# Start the application
# PORT is defined by Cloud Run environment
PORT=${PORT:-8080}
echo "Starting Gunicorn on port ${PORT}..."
exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 --timeout 0 app.main:app
