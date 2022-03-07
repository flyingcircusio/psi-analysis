# Some scripts to analyze PSI Data from Prometheus over Grafana

Set environment variables:

```bash
mv psi.env.sample psi.env
vim psi.env
source psi.env
```

And create some destination folders:

```bash
mkdir data images result
```

Now you can pull in Data

```bash
./pull_in_data.py
```

And create histograms either for all files:

```bash
./analyze_all_in_data.sh
```

Or for a specific file:

```bash
./analyze_data.sh <filename>
```

And then find incidents where a certain value is exceeded:

```bash
./find_incident.py <filename> <value>
```
