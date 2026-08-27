#!/bin/bash
# Script to start RQ scheduler with Redis connection retry

MAX_RETRIES=10
RETRY_DELAY=5

for attempt in $(seq 1 $MAX_RETRIES); do
    echo "Attempt $attempt/$MAX_RETRIES to start scheduler..."
    
    # Try to start the scheduler
    python manage.py rqscheduler default "$@" && exit 0
    
    echo "Scheduler failed, retrying in $RETRY_DELAY seconds..."
    sleep $RETRY_DELAY
done

echo "Max retries reached. Exiting."
exit 1