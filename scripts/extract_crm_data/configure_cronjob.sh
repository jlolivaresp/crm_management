#!/bin/bash

OUTPUT_PATH="./output"

# Define the cron schedule (e.g., 06:00 AM every day)
CRON_SCHEDULE="00 06 * * *"

# Define the script to run
SCRIPT_PATH="$(pwd)/run_main_cli.sh $OUTPUT_PATH"

# Define a unique identifier for the cron job (to avoid duplicates)
CRON_IDENTIFIER="CRM data extraction job"

# Check if the cron job already exists
if crontab -l | grep -q "$CRON_IDENTIFIER"; then
    echo "Cron job already exists. Skipping addition."
else
    # Backup existing crontab
    crontab -l > /tmp/current_cron || true

    # Add the new cron job
    {
        echo "$CRON_SCHEDULE $SCRIPT_PATH $CRON_IDENTIFIER"
    } >> /tmp/current_cron

    # Install the new crontab
    crontab /tmp/current_cron
    echo "Cron job added successfully."
fi

# Cleanup
rm -f /tmp/current_cron
