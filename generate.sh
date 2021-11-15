#!/bin/bash

for dirname in $(ls artifacts/); do
    outdir="docs/_results/${dirname}"
    printf "Checking if we've generated results for ${dirname}\n"
    if [[ ! -d "${outdir}" ]]; then
        printf "python visualize-predictions.py artifacts/$dirname\n"
        python visualize-predictions.py artifacts/$dirname
    else
        printf "$dirname results are already generated.\n"
    fi
done
