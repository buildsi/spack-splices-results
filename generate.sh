#!/bin/bash

for dirname in $(ls artifacts/); do
    printf "python visualize-predictions.py artifacts/$dirname\n"
    python visualize-predictions.py artifacts/$dirname
done
