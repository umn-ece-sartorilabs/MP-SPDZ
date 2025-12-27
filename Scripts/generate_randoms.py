#!/usr/bin/env python3

import random
import argparse

def generate_random_numbers(n, min_val, max_val, output_file):
    with open(output_file, 'w') as f:
        for _ in range(n):
            num = random.randint(min_val, max_val)
            f.write(f"{num} ")

def main():
    parser = argparse.ArgumentParser(description="Generate random numbers and write to a file.")
    parser.add_argument("n", type=int, help="Number of random numbers to generate")
    parser.add_argument("min_val", type=int, help="Minimum value (inclusive)")
    parser.add_argument("max_val", type=int, help="Maximum value (inclusive)")
    parser.add_argument("output_file", type=str, help="Output file name")

    args = parser.parse_args()

    if args.min_val > args.max_val:
        parser.error("min_val should not be greater than max_val")

    generate_random_numbers(args.n, args.min_val, args.max_val, args.output_file)
    print(f"Generated {args.n} numbers in range [{args.min_val}, {args.max_val}] -> {args.output_file}")

if __name__ == "__main__":
    main()