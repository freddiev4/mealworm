#!/bin/bash

# Script to send 10 requests in parallel
# Usage: ./test_parallel_requests.sh [total_requests] [parallel_count]

TOTAL_REQUESTS=${1:-100}
PARALLEL_COUNT=${2:-10}

echo "Sending $TOTAL_REQUESTS requests with $PARALLEL_COUNT parallel requests at a time"
echo "---"

# Function to send a single request
send_request() {
  local request_num=$1
  echo "Request $request_num:"
  curl -X 'POST' \
    'http://localhost:8000/v1/agents/meal_planning_agent/runs' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
  "message": "string",
  "stream": false,
  "model": "gpt-5-mini",
  "user_id": "string",
  "session_id": "string"
}' 2>/dev/null
  echo -e "\n---"
}

# Export the function so it can be used by parallel processes
export -f send_request

# Use xargs to run requests in parallel
seq 1 $TOTAL_REQUESTS | xargs -n 1 -P $PARALLEL_COUNT -I {} bash -c 'send_request {}'

echo "All requests completed!"

