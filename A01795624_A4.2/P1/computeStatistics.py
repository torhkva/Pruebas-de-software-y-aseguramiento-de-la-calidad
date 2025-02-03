"""
Compute Statistics Script

This Python script reads a file containing a list of numbers, computes descriptive statistics,
and saves the results to a file. The computations use only basic algorithms without built-in
statistical functions or libraries.
"""

import sys
import time


def read_numbers(file_path: str):
    """
    Reads numbers from a file and returns a list of valid numbers.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list: A list of valid numbers.
    """
    numbers = []
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                for value in line.split():
                    try:
                        numbers.append(float(value))
                    except ValueError:
                        print(f"Warning: Invalid data '{value}' ignored.")
    except OSError as error:
        print(f"Error reading file: {error}")
        sys.exit(1)
    return numbers


def compute_mean(data: list):
    """Calculates the mean."""
    total = 0
    count = 0
    for num in data:
        total += num
        count += 1
    return total / count if count > 0 else 0


def compute_median(data: list):
    """Calculates the median by sorting and selecting the middle value."""
    n = len(data)
    if n == 0:
        return 0
    sorted_data = data[:]
    for i in range(n - 1):  # We use simple bubble sort
        for j in range(n - i - 1):
            if sorted_data[j] > sorted_data[j + 1]:
                sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]

    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]


def compute_mode(data: list):
    """Calculates the mode by counting occurrences."""
    frequency = {}
    max_count = 0
    mode = None

    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
        if frequency[num] > max_count:
            max_count = frequency[num]
            mode = num
    if max_count == 1:
        return "N/A"
    return mode


def compute_variance(data: list, mean: float):
    """Computes variance."""
    if len(data) < 2:
        return 0
    variance_sum = 0
    for num in data:
        variance_sum += (num - mean) ** 2
    return variance_sum / len(data)


def compute_std_dev(variance: float):
    """Computes standard deviation as the square root of variance."""
    if variance == 0:
        return 0
    x = variance
    guess = x / 2
    while True:  # We implement square root using Newton's method
        new_guess = (guess + x / guess) / 2
        if abs(new_guess - guess) < 1e-6:
            return new_guess
        guess = new_guess


def write_results(mean, median, mode, variance, std_dev, elapsed_time):
    """
    Writes the computed statistics to a file.

    Args:
        mean (float): Computed mean.
        median (float): Computed median.
        mode (float): Computed mode.
        variance (float): Computed variance.
        std_dev (float): Computed standard deviation.
        elapsed_time (float): Execution time.
    """
    try:
        with open('StatisticsResults.txt', 'w', encoding="utf-8") as result_file:
            result_file.write(f"Mean: {mean:.2f}\n")
            result_file.write(f"Median: {median:.2f}\n")
            if mode == "N/A":
                result_file.write(f"Mode: {mode}\n")
            else:
                result_file.write(f"Mode: {mode:.2f}\n")
            result_file.write(f"Variance: {variance:.2f}\n")
            result_file.write(f"Standard Deviation: {std_dev:.2f}\n")
            result_file.write(f"\nTime elapsed: {elapsed_time:.4f} seconds\n")
    except OSError as error:
        print(f"Error writing results: {error}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py <file_with_data.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    start_time = time.time()

    log_numbers = read_numbers(input_file)

    if not log_numbers:
        print("Error: No valid numbers found in the file.")
        sys.exit(1)

    log_mean = compute_mean(log_numbers)
    log_median = compute_median(log_numbers)
    log_mode = compute_mode(log_numbers)
    log_variance = compute_variance(log_numbers, log_mean)
    log_std_dev = compute_std_dev(log_variance)

    log_elapsed_time = time.time() - start_time

    print(f"Mean: {log_mean:.2f}")
    print(f"Median: {log_median:.2f}")
    if log_mode == "N/A":
        print(f"Mode: {log_mode}")
    else:
        print(f"Mode: {log_mode:.2f}")
    print(f"Variance: {log_variance:.2f}")
    print(f"Standard Deviation: {log_std_dev:.2f}")
    print(f"\nElapsed time: {log_elapsed_time:.4f} seconds")

    write_results(log_mean, log_median, log_mode, log_variance, log_std_dev, log_elapsed_time)
