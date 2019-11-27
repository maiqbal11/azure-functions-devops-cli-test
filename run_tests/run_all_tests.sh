#!/bin/bash

set -e -x
export StampAddress=$STAMPADDRESS
python3 -m pip install -r requirements.txt
python3 -m pytest tests
