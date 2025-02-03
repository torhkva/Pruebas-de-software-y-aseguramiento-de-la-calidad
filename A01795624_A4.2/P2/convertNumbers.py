"""
Converter Program

This Python code reads a file containing numbers, converts each number to binary and hexadecimal
using basic algorithms (without built-in functions), and writes the results to a file.
Errors are handled gracefully, and the execution time is recorded.

Usage:
    python convertNumbers.py fileWithData.txt
"""

import sys
import time


def to_binary(num: int) -> str:
    """Converts a decimal number to binary using basic division-by-2 method."""
    if num == 0:
        return "0"
    binary = ""
    while num > 0:
        binary = str(num % 2) + binary
        num //= 2
    return binary


def to_hexadecimal(num: int) -> str:
    """Converts a decimal number to hexadecimal using basic division-by-16 method."""
    if num == 0:
        return "0"
    hex_digits = "0123456789ABCDEF"
    hexadecimal = ""
    while num > 0:
        remainder = num % 16
        hexadecimal = hex_digits[remainder] + hexadecimal
        num //= 16
    return hexadecimal


def process_file(file_path: str):
    """
    Reads numbers from a file, converts them to binary and hexadecimal,
    and writes the results to 'ConvertionResults.txt'.
    Invalid data is logged as an error and skipped.
    """
    results = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                try:
                    number = int(line)
                    binary = to_binary(number)
                    hexadecimal = to_hexadecimal(number)
                    results.append(f"{number} -> Binary: {binary}, Hex: {hexadecimal}")
                except ValueError:
                    print(f"Error: Invalid number on line {line_num}: '{line}'")
    except OSError as error:
        print(f"Error reading file: {error}")
        return []

    # Write results to file
    try:
        with open("ConvertionResults.txt", "w", encoding="utf-8") as result_file:
            for result in results:
                result_file.write(result + "\n")
    except OSError as error:
        print(f"Error writing results: {error}")
        return []

    return results


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py <file_with_data.txt>")
        sys.exit(1)

    input_file = sys.argv[1]

    start_time = time.time()
    output_results = process_file(input_file)
    elapsed_time = time.time() - start_time

    if output_results:
        for output in output_results:
            print(output)

    print(f"\nExecution Time: {elapsed_time:.4f} seconds")

    try:
        with open("ConvertionResults.txt", "a", encoding="utf-8") as log_result_file:
            log_result_file.write(f"\nExecution Time: {elapsed_time:.4f} seconds\n")
    except OSError as error:
        print(f"Error appending execution time: {error}")
