#!/usr/bin/env python3
"""
Generate random 8-bit asset values for the ‘Billionaire’ benchmark.

Each line written to the output file looks like:
    <cash> <property> <stock>

For a given vector_size the file therefore holds
3 × vector_size integers.
"""

import random
import argparse

def generate_records(vector_size: int, min_val: int, max_val: int, output_file: str) -> None:
    """Write <cash prop stock> triples — one per record — to *output_file*."""
    with open(output_file, "w") as f:
        for _ in range(vector_size):
            cash   = random.randint(min_val, max_val)
            prop   = random.randint(min_val, max_val)
            stock  = random.randint(min_val, max_val)
            f.write(f"{cash} {prop} {stock}\n")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate random <cash prop stock> triples for the Billionaire benchmark."
    )
    parser.add_argument("vector_size", type=int, help="Number of records to generate")
    parser.add_argument("min_val",     type=int, help="Minimum value (inclusive)")
    parser.add_argument("max_val",     type=int, help="Maximum value (inclusive)")
    parser.add_argument("output_file", type=str, help="Output file name")

    args = parser.parse_args()

    if args.min_val > args.max_val:
        parser.error("min_val should not be greater than max_val")

    generate_records(args.vector_size, args.min_val, args.max_val, args.output_file)
    print(f"Generated {args.vector_size} records "
          f"(3 × {args.vector_size} = {args.vector_size * 3} numbers) "
          f"in range [{args.min_val}, {args.max_val}] → {args.output_file}")

if __name__ == "__main__":
    main()