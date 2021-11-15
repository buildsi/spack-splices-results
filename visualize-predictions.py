#!/usr/bin/env python

# Usage:
# starting with a results file in your ~/.spack/analyzers/spack-monitor, run as follows:
# python visualize-predictions.py ~/.spack/spack-monitor/analysis/curl/symbolator-predictions.json
# Note the directory name is the package being spliced

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import shutil
import pandas
import sys
import json
import os

here = os.path.dirname(__file__)


def read_json(filename):
    with open(filename, "r") as fd:
        content = json.loads(fd.read())
    return content


template = """---
title: %s results
categories: packages
tags: [package]
permalink: /results/%s/
results:
  %s
maths: 1
toc: 1
---

Splicing %s into binaries for %s. The first plot includes actual outcomes for the commands:

```bash
%s
```

And each following plot below shows predictions for each tester."""


def plot_heatmap(df, save_to=None):
    sns.set_theme(style="white")

    f, ax = plt.subplots(figsize=(30, 30))
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    p = sns.clustermap(
        df, cmap=cmap, center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.5}
    )
    # used for heatmap
    # p.tick_params(labelsize=5)
    # p.set_xlabel("Splice", fontsize=12)
    # p.set_ylabel("Binary", fontsize=12)

    if save_to:
        plt.savefig(save_to)
    return plt


def main(pkg_dir):
    if not os.path.exists(pkg_dir):
        sys.exit("Cannot find %s" % pkg_dir)

    # First assemble unique binary / libs (rows and cols)
    rows = set()  # binaries
    cols = set()  # splices
    testers = set()

    package = os.path.basename(pkg_dir)

    # assumes same command across
    commands = set()

    # First assemble rows and column names
    for version in os.listdir(os.path.abspath(pkg_dir)):
        for result_file in os.listdir(os.path.join(pkg_dir, version)):
            result_file = os.path.join(pkg_dir, version, result_file)
            data = read_json(result_file)

            for datum in data:
                for tester, res in datum["predictions"].items():
                    testers.add(tester)
                    for binary, predictions in res.items():
                        rows.add(binary)
                        for lib, prediction in predictions.items():
                            cols.add(lib)

    print("Found %s testers: %s" % (len(testers), " ".join(testers)))

    # Prepare data frames
    dfs = {"actual": pandas.DataFrame(0, index=rows, columns=cols)}
    for tester in testers:
        dfs[tester] = pandas.DataFrame(0, index=rows, columns=cols)

    for version in os.listdir(os.path.abspath(pkg_dir)):
        for result_file in os.listdir(os.path.join(pkg_dir, version)):
            result_file = os.path.join(pkg_dir, version, result_file)
            data = read_json(result_file)
            for datum in data:
                if commands and datum["command"] not in commands:
                    print("Warning: multiple commands being used for testing!")
                commands.add(datum["command"])

                dfs["actual"].loc[binary][lib] = 1 if datum["actual"] else -1
                for tester, res in datum["predictions"].items():
                    for binary, predictions in res.items():
                        for lib, prediction in predictions.items():
                            prediction = 1 if prediction else -1
                            dfs[tester].loc[binary][lib] = prediction

    # Save results to file under docs
    result_dir = os.path.join(here, "docs", "_results", package)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    listing = ""

    # Save the data frame to file
    count = 0
    for tester, df in dfs.items():

        # Update listing
        if count == 0:
            listing += "- tester: %s\n" % tester
        else:
            listing += "  - tester: %s\n" % tester
        listing += "    png: %s-%s.png\n" % (tester, package)
        listing += "    svg: %s-%s.svg\n" % (tester, package)
        listing += "    pdf: %s-%s.pdf\n" % (tester, package)
        listing += "    csv: %s-%s.csv\n" % (tester, package)

        # Clean up rows / cols
        df.index = ["/".join(x.split("/")[-3:]) for x in list(df.index)]
        df.columns = ["/".join(x.split("/")[-3:]) for x in list(df.columns)]
        result_file = os.path.join(result_dir, "%s-%s.csv" % (tester, package))
        df.to_csv(result_file)
        save_to = os.path.join(result_dir, "%s-%s.pdf" % (tester, package))
        fig = plot_heatmap(df, save_to)

        # save a png and svg too too
        save_to = os.path.join(result_dir, "%s-%s.png" % (tester, package))
        plt.savefig(save_to)
        save_to = os.path.join(result_dir, "%s-%s.svg" % (tester, package))
        plt.savefig(save_to)

        # The splice is derived from columns
        splice = list(df.columns)[0].split("-")[0]
        count += 1

    # Generate a markdown for each
    content = template % (
        package,
        package,
        listing,
        splice,
        package,
        "\n".join(list(commands)),
    )
    md = os.path.join(result_dir, "index.md")
    with open(md, "w") as fd:
        fd.write(content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(
            "Please provide the path to a package folder: python visualize-predictions.py artifacts/curl"
        )
    main(sys.argv[1])
