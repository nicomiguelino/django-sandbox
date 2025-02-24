#!/bin/bash

set -euo pipefail

# Check if Google access token is provided
if [ -z "${GOOGLE_ACCESS_TOKEN:-}" ]; then
    echo "Error: GOOGLE_ACCESS_TOKEN environment variable is required"
    echo "Usage: GOOGLE_ACCESS_TOKEN=your_google_token ./get_calendar_events.sh"
    exit 1
fi

# Google Calendar API endpoint
API_URL="https://www.googleapis.com/calendar/v3/calendars/primary/events"

# Get current time in ISO format
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Make the API call to Google Calendar
response=$(curl -s \
    -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}" \
    -H "Accept: application/json" \
    "${API_URL}?timeMin=${CURRENT_TIME}&maxResults=10&singleEvents=true&orderBy=startTime")

# Check if the call was successful and pretty print the JSON response
if echo "$response" | jq . >/dev/null 2>&1; then
    echo "$response" | jq .
else
    echo "Error: Failed to get calendar events"
    echo "Response: $response"
    exit 1
fi
