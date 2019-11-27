#!/bin/bash

set -e -x
export StampAddress=$STAMPADDRESS
python3 -m pip install pytest requests
python3 -m pytest tests
