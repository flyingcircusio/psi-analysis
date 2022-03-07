#!/usr/bin/env nix-shell
#!nix-shell -i python -p "python3.withPackages (ps: [ ps.requests ])"

"""
Pull in data from https://stats.flyincircus.io/

It's a Grafana host and our API Token is in the environment variable GRAFANA_TOKEN

We're querying from prometheus
"""

import requests
import json
import os
import time
import datetime

GRAFANA_TOKEN = os.environ.get('GRAFANA_TOKEN')
GRAFANA_HOST = os.environ.get('GRAFANA_HOST')
print("Token length:", len(GRAFANA_TOKEN))

DATASOURCE = 18

def get_data(time_in_minutes, metric="psi_cpu", period="avg10", extent="some"):
    """
    Get the data from the last time_in_minutes
    """
    now = int(time.time())
    r = requests.get(
            f"https://{GRAFANA_HOST}/grafana/api/datasources/proxy/{DATASOURCE}/api/v1/query_range",
            params={
                # this is prometheus
                # "query": 'psi_cpu{period="avg10",extent="some"}',
                "query": f'{metric}{{period="{period}",extent="{extent}"}}',
                # 1 day
                "start": str(now - time_in_minutes * 60),
                "end": str(now),
                "step": "1m",
                "format": "json",
            },
            headers = {
                "Authorization": f"Bearer {GRAFANA_TOKEN}",
            },
        )
    print("Query: ", f'{metric}{{period="{period}",extent="{extent}"}}')
    return r.json()


if __name__ == "__main__":
    # # 1 minute
    # data = get_data(1, 'psi_cpu', 'avg10', 'some')
    # with open("psi_cpu-avg10-some-1min.json", "w") as f:
    #     json.dump(data, f)
    
    # # 1 day
    # data = get_data(24*60, 'psi_cpu', 'avg10', 'some')
    # with open("psi_cpu-avg10-some-1day.json", "w") as f:
    #     json.dump(data, f)

    # # 1 week
    # data = get_data(24*60*7, 'psi_cpu', 'avg10', 'some')
    # with open("psi_cpu-avg10-some-1week.json", "w") as f:
    #     json.dump(data, f)

    metrics = ["psi_cpu", "psi_memory", "psi_io"]
    periods = ["avg10", "avg60", "avg300"]
    extents = ["some", "full"]
    tuples = []
    for metric in metrics:
        for period in periods:
            for extent in extents:
                # if cpu, don't do full extent
                if metric == "psi_cpu" and extent == "full":
                    continue
                tuples.append((metric, period, extent))
    
    # for metric, period, extent in tuples:
    #     data = get_data(60, metric, period, extent)
    #     filename = f"data/{metric}-{period}-{extent}-1hour.json"
    #     with open(filename, "w") as f:
    #         json.dump(data, f)

    # 1 day
    for metric, period, extent in tuples:
        data = get_data(24*60, metric, period, extent)
        filename = f"data/{metric}-{period}-{extent}-1day.json"
        with open(filename, "w") as f:
            json.dump(data, f)
