# Quick-Steps-Guide

## Docker Setup

We run a container and mount the MP-SPDZ directory. If the image `mpc-frameworks` already exist we directly launch a container, else we build the image and then launch the container.

```
./setup_docker.sh
```

This script will use the modified `Dockerfile` to build the image with the required packages.

## Setup Instructions


0. (OPTIONAL) If using a Release Build use the following script to complete the setup, else skip this.
    ```
    Scripts/tldr.sh
    ```
1. Inside the Docker container, navigate to the MP-SPDZ directory,
    ```
    cd /workspace/MP-SPDZ
    ```

2. Update all the submodules 
    ```
    git submodule update --init --recursive
    ```

3. Setup SSL for 2-Parties

    ```
    Scripts/setup-ssl.sh 2
    ```

## Compile the Protocols

Protocols can be found in the  `MP-SPDZ/Makefile`

Usage:
```
make -j `nproc` <protocol>
```

Example:
```
make -j `nproc` mascot-party.x
make -j `nproc` semi2k-party.x
```

## Compile the Programs

Usage:
```
./compile.py <program> <argument|benchmark> <vector_size> <repetitions>
```

Example:
```
./compile.py benchmarks sum 32 1
```

Note (1): Compile Count, ReLU, Billionaire benchmark using modulo prime field for **Mascot** 
```
./compile.py benchmarks <count|relu|billionaire> 32 1
```

Note (2): Compile Count, ReLU, Billionaire benchmark using modulo 2k Ring for **Semi2k** 
```
./compile.py -R 64 benchmarks <count|relu|billionaire> 32 1
```

This will write to `Programs/Schedules/<program>-<argument benchmark>-<vector_size>-<repetitions>.sch`

This will write to `Programs/Bytecode/<program>-<argument benchmark>-<vector_size>-<repetitions>-0.bc`

## Setup Input Vectors

1) Random Numbers (for sum, count, ReLU) can be generated using a Python script `Scripts/generate_randoms.py`

    Usage:
    ```
    Scripts/generate_randoms.py <vector_size> <min> <max> <output_file>
    ```

    Example:
    ```
    Scripts/generate_randoms.py 32 -1000 1000 Player-Data/Input-P0-0
    Scripts/generate_randoms.py 32 -1000 1000 Player-Data/Input-P1-0
    ```

2) Random Numbers (for billionaire) can be generated using a Python script `Scripts/generate_wealth.py`

    Usage:
    ```
    Scripts/generate_wealth.py <vector_size> <min> <max> <output_file>
    ```

    Example:
    ```
    Scripts/generate_wealth.py 32 0 1000000000 Player-Data/Input-P0-0
    Scripts/generate_wealth.py 32 0 1000000000 Player-Data/Input-P1-0
    ```

## Run the Program(s)

Usage:
```
Scripts/<protocol>.sh <program>-<argument|benchmark>-<vector_size>-<repetitions>
```
**Optional Argument** `-v` for verbose output

Example:
```
Scripts/mascot.sh benchmarks-sum-512-1
Scripts/semi2k.sh -v benchmarks-count-32-1
```

#### Sample Run Scripts can be found here

```
Scripts/run_relu.sh
Scripts/run_billionaire.sh
```