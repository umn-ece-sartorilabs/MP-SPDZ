# Multi-Protocol SPDZ [![Documentation Status](https://readthedocs.org/projects/mp-spdz/badge/?version=latest)](https://mp-spdz.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://dev.azure.com/data61/MP-SPDZ/_apis/build/status/data61.MP-SPDZ?branchName=master)](https://dev.azure.com/data61/MP-SPDZ/_build/latest?definitionId=7&branchName=master) [![Gitter](https://badges.gitter.im/MP-SPDZ/community.svg)](https://gitter.im/MP-SPDZ/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

This is a software to benchmark various secure multi-party computation (MPC) protocols in a variety of security models such as honest and dishonest majority, semi-honest/passive and malicious/active corruption. The underlying technologies span secret sharing, homomorphic encryption, and garbled circuits.

## Quick Setup

### 1. Docker Setup

Run the setup script from the MPC-Frameworks parent directory:

```bash
./setup_docker.sh
```

This builds a Docker image with all required dependencies.

### 2. Initialize Environment

Inside the Docker container:

```bash
cd /workspace/MP-SPDZ

# Update all submodules
git submodule update --init --recursive

# Setup SSL certificates for 2-party computation
Scripts/setup-ssl.sh 2
```

### 3. Compile Protocol Virtual Machines

Compile the required protocols (choose one or both):

```bash
# For Semi2k (modulo 2^k)
make -j `nproc` semi2k-party.x

# For Mascot (modulo prime)
make -j `nproc` mascot-party.x
```

## Available Protocols

MP-SPDZ supports multiple protocols across different security models:

### Dishonest Majority Protocols

| Program | Protocol | Domain | Security | Players | Script |
|---------|----------|--------|----------|---------|--------|
| `mascot-party.x` | MASCOT | Mod prime | Malicious | 2+ | `mascot.sh` |
| `spdz2k-party.x` | SPDZ2k | Mod 2^k | Malicious | 2+ | `spdz2k.sh` |
| `semi-party.x` | OT-based | Mod prime | Semi-honest | 2+ | `semi.sh` |
| `semi2k-party.x` | OT-based | Mod 2^k | Semi-honest | 2+ | `semi2k.sh` |
| `semi-bin-party.x` | OT-based | Binary | Semi-honest | 2+ | `semi-bin.sh` |
| `tiny-party.x` | Adapted SPDZ2k | Binary | Malicious | 2+ | `tiny.sh` |
| `lowgear-party.x` | LowGear | Mod prime | Malicious | 2+ | `lowgear.sh` |
| `highgear-party.x` | HighGear | Mod prime | Malicious | 2+ | `highgear.sh` |

### Honest Majority Protocols

| Program | Protocol | Domain | Security | Players | Script |
|---------|----------|---------|----------|---------|--------|
| `replicated-ring-party.x` | Replicated | Mod 2^k | Semi-honest | 3 | `ring.sh` |
| `brain-party.x` | Replicated | Mod 2^k | Malicious | 3 | `brain.sh` |
| `replicated-field-party.x` | Replicated | Mod prime | Semi-honest | 3 | `rep-field.sh` |
| `malicious-rep-field-party.x` | Replicated | Mod prime | Malicious | 3 | `mal-rep-field.sh` |
| `sy-rep-field-party.x` | SPDZ-wise | Mod prime | Malicious | 3 | `sy-rep-field.sh` |
| `shamir-party.x` | Shamir | Mod prime | Semi-honest | 3+ | `shamir.sh` |
| `malicious-shamir-party.x` | Shamir | Mod prime | Malicious | 3+ | `mal-shamir.sh` |
| `rep4-ring-party.x` | Replicated | Mod 2^k | Malicious | 4 | `rep4-ring.sh` |

**Note:** Compile protocols with `make -j \`nproc\` <protocol-name>`

## Compiling High-Level Programs

MP-SPDZ programs are written in a Python-like language and must be compiled to bytecode before execution.

### Compilation Options by Domain

#### 1. Arithmetic Modulo a Prime

```bash
./compile.py [-F <integer_bit_length>] [-P <prime>] <program>
```

**Examples:**
```bash
./compile.py tutorial                    # Default: 64-bit integers
./compile.py -F 128 tutorial             # 128-bit integers
./compile.py -F 64 -P 2305843009213693951 tutorial  # Specific prime
```

#### 2. Arithmetic Modulo 2^k (Ring)

```bash
./compile.py -R <bit_length> <program>
```

**Examples:**
```bash
./compile.py -R 64 tutorial              # 64-bit ring
./compile.py -R 128 tutorial             # 128-bit ring
```

#### 3. Binary Circuits

```bash
./compile.py -B <integer_bit_length> <program>
```

**Examples:**
```bash
./compile.py -B 32 tutorial              # 32-bit binary
./compile.py -B 64 tutorial              # 64-bit binary
```

#### 4. Mixed Circuits (Arithmetic + Binary)

Enable mixed-circuit computation for non-linear operations:

```bash
./compile.py -X -F 64 <program>          # Classic daBits (mod prime)
./compile.py -Y -F 64 <program>          # Extended daBits (mod prime)
./compile.py -X -R 64 <program>          # Classic daBits (mod 2^k)
```

### Common Compilation Flags

| Flag | Description |
|------|-------------|
| `-F <n>` | Integer bit length for prime field (default: 64) |
| `-R <n>` | Ring size (mod 2^n) |
| `-B <n>` | Binary circuit with n-bit integers |
| `-P <p>` | Specific prime modulus |
| `-X` | Enable classic daBits for mixed circuits |
| `-Y` | Enable extended daBits for mixed circuits |
| `-Z <n>` | Local share conversion (n parties) |
| `-G` | Compile for garbled circuits |
| `-O` | Optimize compilation |

### Program Arguments

Compile programs with arguments:

```bash
./compile.py <program> <arg1> <arg2> ...
```

**Example:**
```bash
./compile.py benchmarks sum 32 1
# Creates: Programs/Bytecode/benchmarks-sum-32-1-0.bc
```

## Running Benchmarks

MP-SPDZ includes four standard benchmarks: **sum**, **count**, **relu**, and **billionaire**.

### Compile Benchmarks

**For Mascot (modulo prime):**
```bash
./compile.py benchmarks sum 32 1
./compile.py benchmarks count 32 1
./compile.py benchmarks relu 32 1
./compile.py benchmarks billionaire 32 1
```

**For Semi2k (modulo 2^64):**
```bash
./compile.py -R 64 benchmarks sum 32 1
./compile.py -R 64 benchmarks count 32 1
./compile.py -R 64 benchmarks relu 32 1
./compile.py -R 64 benchmarks billionaire 32 1
```

**Parameters:**
- `32` = vector size
- `1` = number of repetitions

> **Important Notes:**
> 
> **Note (1):** Compile **Count**, **ReLU**, and **Billionaire** benchmarks using modulo prime field (without `-R` flag) for **Mascot** and other protocols that use modulo prime (e.g., `semi-party.x`, `lowgear-party.x`, `highgear-party.x`, `replicated-field-party.x`, `shamir-party.x`).
> 
> **Note (2):** Compile **Count**, **ReLU**, and **Billionaire** benchmarks using modulo 2^k ring (with `-R 64` flag) for **Semi2k** and other protocols that use modulo 2^k ring (e.g., `spdz2k-party.x`, `replicated-ring-party.x`, `brain-party.x`, `rep4-ring-party.x`).
>
> The **Sum** benchmark works with both compilation modes.

### Generate Input Data

**For sum, count, and relu benchmarks:**
```bash
Scripts/generate_randoms.py 32 -1000 1000 Player-Data/Input-P0-0
Scripts/generate_randoms.py 32 -1000 1000 Player-Data/Input-P1-0
```

**For billionaire benchmark:**
```bash
Scripts/generate_wealth.py 32 0 1000000000 Player-Data/Input-P0-0
Scripts/generate_wealth.py 32 0 1000000000 Player-Data/Input-P1-0
```

### Execute Benchmarks

**Run with Mascot:**
```bash
Scripts/mascot.sh benchmarks-sum-32-1
Scripts/mascot.sh benchmarks-count-32-1
Scripts/mascot.sh benchmarks-relu-32-1
Scripts/mascot.sh benchmarks-billionaire-32-1
```

**Run with Semi2k:**
```bash
Scripts/semi2k.sh benchmarks-sum-32-1
Scripts/semi2k.sh benchmarks-count-32-1
Scripts/semi2k.sh benchmarks-relu-32-1
Scripts/semi2k.sh benchmarks-billionaire-32-1
```

**Add `-v` for verbose output:**
```bash
Scripts/semi2k.sh -v benchmarks-count-32-1
```

## Running Computations

There are three main ways to run MPC computations:

### Method 1: Separate Compilation and Execution (Recommended)

Compile once, run multiple times:

```bash
# Step 1: Compile the program
./compile.py -R 64 tutorial

# Step 2: Run with desired protocol (can run multiple times)
Scripts/semi2k.sh tutorial
Scripts/semi2k.sh tutorial  # Run again with different inputs
```

### Method 2: Local Execution (One Command)

Automatically compiles and runs locally:

```bash
Scripts/compile-run.py -E mascot tutorial
Scripts/compile-run.py -E semi2k tutorial -- <runtime-args>
```

**Available protocol names:** `mascot`, `semi2k`, `semi`, `spdz2k`, `ring`, `brain`, `shamir`, etc.

### Method 3: Remote Execution

Compile, upload, and execute on remote hosts via SSH:

```bash
# Create a HOSTS file with format:
# [user@]host0[/path]
# [user@]host1[/path]

Scripts/compile-run.py -H HOSTS -E mascot tutorial -- <runtime-args>
```

**HOSTS file example:**
```
alice@192.168.1.10/mpspdz
bob@192.168.1.11/mpspdz
```

**Note:** SSH key-based authentication must be configured.

### Running on Single Machine

#### Interactive Mode (with `-I` flag)

Players are prompted for inputs during runtime:

```bash
# Terminal 1 (Party 0)
./mascot-party.x -N 2 -I -p 0 tutorial

# Terminal 2 (Party 1)
./mascot-party.x -N 2 -I -p 1 tutorial
```

#### Non-Interactive Mode (reads from files)

Inputs are read from `Player-Data/Input-P<party>-0`:

```bash
# Terminal 1 (Party 0)
./mascot-party.x -N 2 -p 0 tutorial

# Terminal 2 (Party 1)
./mascot-party.x -N 2 -p 1 tutorial
```

**Or use the convenience script:**
```bash
Scripts/mascot.sh tutorial
```

### Running on Multiple Machines

Specify the hostname where party 0 runs:

```bash
# On machine 'alice' (Party 0)
./mascot-party.x -N 2 -h alice -p 0 tutorial

# On machine 'bob' (Party 1)
./mascot-party.x -N 2 -h alice -p 1 tutorial
```

### Common Runtime Options

| Option | Description |
|--------|-------------|
| `-N <n>` | Number of parties |
| `-p <n>` | Player number (0-indexed) |
| `-h <host>` | Hostname of party 0 |
| `-pn <port>` | Base port number (default: 5000) |
| `-I` | Interactive mode (prompt for inputs) |
| `-v` | Verbose output |
| `-F` | Read preprocessing from files |

### Example: Running 3-Party Honest Majority

```bash
# Compile for replicated secret sharing
./compile.py -R 64 tutorial

# Setup SSL for 3 parties (if not done)
Scripts/setup-ssl.sh 3

# Run on single machine
Scripts/ring.sh tutorial

# Or manually in three terminals
./replicated-ring-party.x -I -p 0 tutorial
./replicated-ring-party.x -I -p 1 tutorial
./replicated-ring-party.x -I -p 2 tutorial
```

### Input/Output Files

**Input files location:**
```
Player-Data/Input-P<party>-<thread>
```

**Example input file format (one value per line):**
```
42
17
99
```

**Output:** Printed to console or can be redirected

### Network Configuration

**Default ports:** MP-SPDZ uses TCP ports starting from 5000

**Change base port:**
```bash
./mascot-party.x -N 2 -pn 6000 -p 0 tutorial  # Uses ports 6000+
```

**SSL certificates:** Required for honest majority protocols
- Location: `Player-Data/P<i>.key` and `Player-Data/P<i>.pem`
- Generate with: `Scripts/setup-ssl.sh <num_parties>`

## Example Workflow

```bash
# 1. Enter Docker container
cd /workspace/MP-SPDZ

# 2. Initialize
git submodule update --init --recursive
Scripts/setup-ssl.sh 2

# 3. Compile protocols
make -j `nproc` semi2k-party.x mascot-party.x

# 4. Compile a benchmark (e.g., sum with Semi2k)
./compile.py -R 64 benchmarks sum 32 1

# 5. Generate inputs
Scripts/generate_randoms.py 32 -1000 1000 Player-Data/Input-P0-0
Scripts/generate_randoms.py 32 -1000 1000 Player-Data/Input-P1-0

# 6. Run the benchmark
Scripts/semi2k.sh benchmarks-sum-32-1
```

## Benchmark Scripts

Pre-configured scripts are available for common workflows:

```bash
Scripts/run_relu.sh
Scripts/run_billionaire.sh
```

## Output Files

Compilation generates:
- **Bytecode:** `Programs/Bytecode/<program>-<benchmark>-<size>-<reps>-0.bc`
- **Schedule:** `Programs/Schedules/<program>-<benchmark>-<size>-<reps>.sch`

## Additional Resources

- **Full Documentation:** https://mp-spdz.readthedocs.io
- **Frequently Asked Questions:** https://mp-spdz.readthedocs.io/en/latest/troubleshooting.html
- **Paper:** [MP-SPDZ Framework](https://eprint.iacr.org/2020/521)
- **Issues:** https://github.com/data61/MP-SPDZ/issues

## Contact and Support

### Reporting Issues

[Filing an issue on GitHub](https://github.com/data61/MP-SPDZ/issues) is the preferred way of contacting us, but you can also write an email to [mp-spdz@googlegroups.com](mailto:mp-spdz@googlegroups.com) ([archive](https://groups.google.com/forum/#!forum/mp-spdz)).

Before reporting a problem, please check the list of [known issues and possible solutions](https://mp-spdz.readthedocs.io/en/latest/troubleshooting.html).

**When filing issues, please include:**
- Complete code examples (incomplete code cannot be reproduced)
- Which protocol you used (protocols differ considerably)
- Error messages and relevant output
- Your system configuration (OS, compiler version, etc.)

## Citation

The design of MP-SPDZ is described in [this paper](https://eprint.iacr.org/2020/521). If you use it for an academic project, please cite:

```bibtex
@inproceedings{mp-spdz,
    author = {Marcel Keller},
    title = {{MP-SPDZ}: A Versatile Framework for Multi-Party Computation},
    booktitle = {Proceedings of the 2020 ACM SIGSAC Conference on
    Computer and Communications Security},
    year = {2020},
    doi = {10.1145/3372297.3417872},
    url = {https://doi.org/10.1145/3372297.3417872},
}
```