#!/bin/bash

if [ -z ${INPUT_PACKAGE+x} ]; then 
    for dirname in $(ls artifacts/); do
        printf "python visualize-predictions.py artifacts/$dirname\n"
        python visualize-predictions.py artifacts/$dirname
    done   
else 
    printf "python visualize-predictions.py artifacts/${INPUT_PACKAGE}\n"
    python visualize-predictions.py artifacts/${INPUT_PACKAGE}
fi
