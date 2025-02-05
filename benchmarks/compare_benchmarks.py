#!/usr/bin/env python3
import os
import subprocess
import re
import statistics
import shutil
import argparse
import sys

LOGDIR = "/tmp/erasan_benchmark_logs"
CWD = os.path.dirname(os.path.realpath(__file__))

# Define the subdirectories and configurations
benchmarks = ["smallvec", "itoa", "semver", "strsim", "unicode"]

def run_benchmarks(subdir, config) -> list[float]:
    path = os.path.join(CWD, subdir, "test", config)
    binary = os.path.join(path, config)
    if not os.path.isfile(binary):
        print(f"Error: Binary not found: {binary}")
        exit(1)

    print(f"Running benchmark: {subdir}, Configuration: {config} in path: {path}")
    result = subprocess.run([binary, "--bench"], capture_output=True, text=True, cwd=path)
    # log output to file in directory "logs", create directory if it does not exist
    
    if not os.path.exists(LOGDIR):
        os.makedirs(LOGDIR)
    stdout_file = os.path.join(LOGDIR, f"log_{subdir}_{config}.log.stdout")
    stderr_file = os.path.join(LOGDIR, f"log_{subdir}_{config}.log.stderr")

    with open(stdout_file, "a") as logfile:
        logfile.write(result.stdout + "\n")
    with open(stderr_file, "a") as logfile:
        logfile.write(result.stderr + "\n")
    if result.returncode != 0:
        if result.returncode == 101:
            print(f"Some benchmarks of {subdir} (Configuration: {config}) failed.")
        else:
            print(f"Failed to run benchmark: {subdir}, Configuration: {config}")
            exit(1)

    return parse_benchmarks_output(result.stdout)

def parse_benchmarks_output(output: str) -> list[float]:
    pattern = re.compile(r"\ntest ([^ ]+) +\.\.\. bench: +([0-9,]+) ns/iter \(\+/- ([0-9,]+)\)")
    runtimes = []
    for item in pattern.finditer(output):
        runtime_str = item.group(2).replace(",", "") # remove thousands seperators from number
        runtime = float(runtime_str)
        runtimes.append(runtime)
    print(runtimes)
    return runtimes

def read_benchmarks_from_logs(subdir, config) -> list[float]:
    stdout_file = os.path.join(LOGDIR, f"log_{subdir}_{config}.log.stdout")
    if not os.path.isfile(stdout_file):
        print(f"Error: Log file not found: {stdout_file}")
        exit(1)
    with open(stdout_file, "r") as logfile:
        output = logfile.read()
    return parse_benchmarks_output(output)

def main():
    read_from_logs = False
    if len(sys.argv) > 1: 
        if sys.argv[1] == "--read-from-logs":
            read_from_logs = True
        else:
            print("Error: Invalid argument")
            print("Usage: compare_benchmarks.py [--read-from-logs]")
            exit(1)


    if not read_from_logs:
        # remove old logs
        if os.path.exists(LOGDIR):
            shutil.rmtree(LOGDIR)
    
    arithmean_overheads_per_benchmark = {}
    geommean_overheads_per_benchmark = {}
    for benchmark in benchmarks:
        if read_from_logs:
            runtimes_native = read_benchmarks_from_logs(benchmark, "native")
            runtimes_erasan = read_benchmarks_from_logs(benchmark, "erasan")
        else:
            runtimes_native = run_benchmarks(benchmark, "native")
            runtimes_erasan = run_benchmarks(benchmark, "erasan")
        assert(len(runtimes_native) == len(runtimes_erasan))
        overheads = [erasan / native for native, erasan in zip(runtimes_native, runtimes_erasan) if native != 0]
        print(f"ERASan overheads for benchmark {benchmark}: {overheads}")
        arithmetic_mean = statistics.mean(overheads)
        geometric_mean = statistics.geometric_mean(overheads)
        arithmean_overheads_per_benchmark[benchmark] = arithmetic_mean
        geommean_overheads_per_benchmark[benchmark] = geometric_mean
    
    # print table with overheads per benchmark
    print("Benchmark | Arithmetic Mean | Geometric Mean")
    print("----------|-----------------|---------------")
    for benchmark in benchmarks:
        print(f"{benchmark:>9} | {arithmean_overheads_per_benchmark[benchmark]:>15.2f} | {geommean_overheads_per_benchmark[benchmark]:>13.2f}")


def test():
    output = """
test bench_itoa_format::bench_i16_0    ... bench:           0 ns/iter (+/- 0)
test bench_itoa_format::bench_i16_min  ... bench:           1 ns/iter (+/- 0)
test bench_itoa_format::bench_u128_0   ... bench:           2 ns/iter (+/- 0)
test bench_itoa_format::bench_u128_max ... bench:          14 ns/iter (+/- 0)
test bench_itoa_format::bench_u64_0    ... bench:           0 ns/iter (+/- 0)
test bench_itoa_format::bench_u64_half ... bench:           2 ns/iter (+/- 0)
test bench_itoa_format::bench_u64_max  ... bench:           4 ns/iter (+/- 0)
test bench_std_fmt::bench_i16_0        ... bench:          14 ns/iter (+/- 0)
test bench_std_fmt::bench_i16_min      ... bench:          24 ns/iter (+/- 0)
test bench_std_fmt::bench_u128_0       ... bench:          16 ns/iter (+/- 1)
test bench_std_fmt::bench_u128_max     ... bench:          35 ns/iter (+/- 0)
test bench_std_fmt::bench_u64_0        ... bench:          14 ns/iter (+/- 1)
test bench_std_fmt::bench_u64_half     ... bench:          15 ns/iter (+/- 0)
test bench_std_fmt::bench_u64_max      ... bench:          16 ns/iter (+/- 0)
"""
    pattern = re.compile(r"\ntest ([^ ]+) +\.\.\. bench: +([0-9,]+) ns/iter \(\+/- ([0-9,]+)\)")
    for item in pattern.finditer(output):
        print(f"{item.group(1)}--------{item.group(2)}-----------{item.group(3)}")

if __name__ == "__main__":
    main()