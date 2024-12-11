#!/bin/bash

OUTPUT_PATH=$1

docker run --rm  -v "$OUTPUT_PATH:/app/output" crm-extraction-cli "scripts/extract_crm_data/main.py"