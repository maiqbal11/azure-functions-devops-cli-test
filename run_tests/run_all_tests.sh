#!/bin/bash

set -e -x
export StampAddress=$STAMPADDRESS
python -m pip install pytest requests
pytest tests
