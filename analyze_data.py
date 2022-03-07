#!/usr/bin/env nix-shell
#!nix-shell -i python -p "python3.withPackages (ps: [ ps.matplotlib ps.numpy ])"

import matplotlib.pyplot as plt
import numpy as np
import json
import os
import time
import datetime
import argparse


if __name__ == "__main__":
    # read filename from argument
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="filename to read")
    args = parser.parse_args()
    file = args.filename
    filename = os.path.basename(file)

    # the filename is in the format {metric}-{period}-{extent}-{timescale}.json
    # so let's parse it
    metric, period, extent, timescale = filename.split("-")
    # timescale has .json at the end so we remove it
    timescale = timescale.replace(".json", "")

    # read data from file
    with open(file, "r") as f:
        data = json.load(f)
    
    # relevant values are in .data.result[].values[][1]
    # .data.result[].values[][0] is the timestamp but we don't need it

    # read
    values = []
    for result in data["data"]["result"]:
        for value in result["values"]:
            # parse the string
            value = value[1]
            value = float(value)
            values.append(value)
    
    # sort
    values.sort()

    # we want to read the percentiles so we calculate a number from 0 to 1 for each value
    xs = np.arange(len(values)) / len(values)
    # plot
    plt.plot(xs, values)
    plt.title(f"{metric} {period} {extent} {timescale}")
    plt.xlabel("percentile")
    plt.ylabel(f"{metric}")

    # add a point at 0.95, and whatever the value is
    x95 = np.arange(0, 1, 1/len(values))[int(0.95*len(values))]
    y95 = values[int(0.95*len(values))]
    plt.plot(x95, y95, "ro")
    plt.annotate(
        f"95th percentile: {y95}",
        xy=(x95, y95),
        xytext=(x95-0.2, y95+10),
        arrowprops=dict(facecolor='black', shrink=0.05),
        horizontalalignment='right',
        verticalalignment='top',
        clip_on=True,
    )

    # also 99th percentile
    x99 = np.arange(0, 1, 1/len(values))[int(0.99*len(values))]
    y99 = values[int(0.99*len(values))]
    plt.plot(x99, y99, "ro")
    plt.annotate(
        f"99th percentile: {y99}",
        xy=(x99, y99),
        xytext=(x99-0.2, y99+20),
        arrowprops=dict(facecolor='black', shrink=0.05),
        horizontalalignment='right',
        verticalalignment='top',
        clip_on=True,
    )

    # save to images/
    plt.savefig(f"images/{metric}-{period}-{extent}-{timescale}.png")
    # plt.show()

