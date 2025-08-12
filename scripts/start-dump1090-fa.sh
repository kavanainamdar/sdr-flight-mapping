#!/bin/bash

# === Configuration ===
# Path to the directory where dump1090-fa will write JSON data
DATA_JSON_PATH="../data/"
JSON_LOCATION_ACCURACY=1

sudo dump1090-fa --interactive --net --write-json ${DATA_JSON_PATH} \
    --json-location-accuracy ${JSON_LOCATION_ACCURACY}
