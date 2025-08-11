# Task 1: LRU Cache for Range Sum Queries Optimization

This project demonstrates how an **LRU (Least Recently Used) cache** can significantly speed up repeated "hot" queries for sum ranges in a large array of integers.

## Description

We have an array of positive integers and need to process two types of queries:

- `Range(L, R)`: Compute the sum of elements from index `L` to `R` inclusive.
- `Update(index, value)`: Update the element at `index` with a new `value`.

The array can be very large (up to 100,000 elements), and the number of queries is also large (up to 50,000).

To speed up processing, we implement an LRU cache that stores results of recent `Range` sum queries. When an element is updated, the cache invalidates all stored sums that include that element's index.

## Features

- Custom implementation of an **LRU cache** using `OrderedDict` for efficient caching of range sums.
- Selective invalidation of cache entries when array updates affect cached ranges.
- Simulation of realistic query workloads including "hot" frequently accessed ranges.
- Performance comparison between uncached and cached query processing.

## How It Works

1. **Without cache** — each `Range` query computes the sum by iterating over the array slice.
2. **With cache** — results of recent `Range` queries are cached. Cache hit returns the stored sum immediately.
3. On `Update`, only cached ranges covering the updated index are invalidated, preserving other cached sums.

## Usage

Run the test script:

```bash
python lru_range_sum.py
```
## Result

![Logistics Network Graph](results/lru_cache.jpg)

---

# Task 2: Fibonacci Performance Comparison: LRU Cache vs Splay Tree

## Overview

This project implements two different approaches to computing Fibonacci numbers with memoization to improve performance:

- **LRU Cache Approach:** Uses Python's built-in `@lru_cache` decorator to automatically cache previously computed Fibonacci values.
- **Splay Tree Approach:** Uses a self-implemented Splay Tree data structure to store and retrieve previously computed Fibonacci numbers.

The goal is to compare the performance of these two caching mechanisms by measuring the average execution time of calculating Fibonacci numbers for various inputs.

---

## Features

- Two Fibonacci implementations:
  - `fibonacci_lru(n)` — recursive function with `@lru_cache`.
  - `fibonacci_splay(n, tree)` — recursive function using a custom Splay Tree as cache.
  
- Performance measurement:
  - Measures average execution time for each approach using Python's `timeit` module.
  - Tests inputs from 0 to 350 (inclusive) stepping by 50.
  
- Output:
  - Prints a formatted table of results showing execution times for each method.
  - Plots a comparison graph of execution times using `matplotlib`.

---

## Installation

1. Ensure you have Python 3.7+ installed.
2. Install required packages:
```bash
pip install matplotlib
```
## Usage

Run the test script:

```bash
python fibonacci.py
```

## Result

![Logistics Network Graph](results/fibonacci.jpg)
