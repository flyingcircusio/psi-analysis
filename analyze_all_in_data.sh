# for each file in data/
# run analyze_data.py on it

for file in data/*.json
do
    echo "analyzing $file"
    ./analyze_data.py $file
done

