#!/bin/bash

#docker run --rm crm-extraction-cli "$@"

echo "$@"

docker run crm-extraction-cli "scripts/update_domain_value/main.py" "$@"