#!/bin/bash
# Script to start RQ worker with Redis connection retry

MAX_RETRIES=10
RETRY_DELAY=5

for attempt in $(seq 1 $MAX_RETRIES); do
    echo "Attempt $attempt/$MAX_RETRIES to start worker..."
    
    # Try to start the worker with empty sentry-dsn to avoid errors
    python manage.py rqworker default --sentry-dsn="" "$@" && exit 0
    
    echo "Worker failed, retrying in $RETRY_DELAY seconds..."
    sleep $RETRY_DELAY
done

echo "Max retries reached. Exiting."
exit 1