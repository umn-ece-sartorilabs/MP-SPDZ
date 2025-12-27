#!/bin/bash

# rm -rf MASCOT/* Semi2k/* Programs/Bytecode/* Programs/Schedules/*
# rm sum* relu* count* billion*

# Check if the correct number of arguments is passed
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <vector_size>"
    exit 1
fi

# Run Script for the various benchmarks (make sure you have completed all pervious steps)

rm -rf Player-Data

mkdir Player-Data
mkdir -p MASCOT
mkdir -p Semi2k

## Vector Size
vector_size="$1"
Scripts/generate_wealth.py "$vector_size" 0 1000000000 Player-Data/Input-P0-0
Scripts/generate_wealth.py "$vector_size" 0 1000000000 Player-Data/Input-P1-0


#### BENCHMARK - Billionaire
./compile.py benchmarks billionaire "$vector_size" 1 > billionaire-"$vector_size".log &
wait
Scripts/mascot.sh benchmarks-billionaire-"$vector_size"-1 > MASCOT/billionaire-"$vector_size".log &
wait
./compile.py -R 64 benchmarks billionaire "$vector_size" 1 > billionaire-"$vector_size".log &
wait
Scripts/semi2k.sh benchmarks-billionaire-"$vector_size"-1 > Semi2k/billionaire-"$vector_size".log &
wait
#### Teardown Vectors
rm -rf Player-Data/*