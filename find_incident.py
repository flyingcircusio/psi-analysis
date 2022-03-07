#!/usr/bin/env nix-shell
#!nix-shell -i python -p "python3.withPackages (ps: [ ps.numpy ])"

import numpy as np
import json
import os
import time
import argparse
import datetime

if __name__ == "__main__":
    """
    read filename from arguments
    read limit value from arguments
    read data values from file
    show hosts and times when the value is above the limit
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="filename to read")
    parser.add_argument("limit", help="limit value")
    args = parser.parse_args()
    file = args.filename
    limit = float(args.limit)
    filename = os.path.basename(file)

    # the filename is in the format {metric}-{period}-{extent}-{timescale}.json
    # so let's parse it
    metric, period, extent, timescale = filename.split("-")
    # timescale has .json at the end so we remove it
    timescale = timescale.replace(".json", "")

    # read data from file
    with open(file, "r") as f:
        data = json.load(f)
    
    # host is in .data.result[].metric.host
    # timestamps are in .data.result[].values[][0]
    # values are in .data.result[].values[][1]
    # our ideal value would be {host: [(timestamp, value)]}
    # so let's parse it

    # read
    values = {}
    for result in data["data"]["result"]:
        host = result["metric"]["host"]
        for value in result["values"]:
            # parse the string
            timestamp = value[0]
            timestamp = datetime.datetime.fromtimestamp(int(timestamp))
            value = value[1]
            value = float(value)
            values[host] = values.get(host, []) + [(timestamp, value)]
    
    # so let's loop through the values and find the ones that are above the limit
    # our result would be {host: [(start_time, end_time), ...]}
    result = {}
    for host, host_values in values.items():
        is_above_limit = False
        start_time = None
        end_time = None
        for timestamp, value in host_values:
            if is_above_limit:
                if value < limit:
                    end_time = timestamp
                    is_above_limit = False
                    result[host] = result.get(host, [])
                    result[host].append((start_time, end_time))
            else:
                if value >= limit:
                    start_time = timestamp
                    is_above_limit = True
        if is_above_limit:
            result[host] = result.get(host, [])
            result[host].append((start_time, host_values[-1][0]))
        
    # print the result
    for host, times in result.items():
        print(f"{host}")
        for start_time, end_time in times:
            print(f"  {start_time} - {end_time}")

    # write the result to a file in result/
    with open(f"result/{metric}-{period}-{extent}-{timescale}.txt", "w") as f:
        for host, times in result.items():
            for start_time, end_time in times:
                f.write(f"{host} {start_time} {end_time}\n")