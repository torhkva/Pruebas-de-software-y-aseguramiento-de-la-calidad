"""
Word Count Script

This Python script reads a file, counts word occurrences, and saves the results to a file.
"""

import sys
import time

def count_words(file_path):
    """
    Counts occurrences of words in a given text file without using built-in string functions.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        dict: A dictionary containing words as keys and their frequencies as values.
    """
    word_frequencies = {}

    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                words = line.split()
                for raw_word in words:
                    cleaned_word = ''.join(
                        char.lower() if 'A' <= char <= 'Z' or 'a' <= char <= 'z' else ''
                        for char in raw_word
                    )

                    if cleaned_word:
                        word_frequencies[cleaned_word] = word_frequencies.get(cleaned_word, 0) + 1
    except OSError as error:
        print(f"Error reading file: {error}")

    return word_frequencies


def write_results(results, elapsed_time):
    """
    Writes word count results and execution time to a file.

    Args:
        results (dict): A dictionary containing word frequencies.
        elapsed_time (float): Execution time.
    """
    try:
        with open('WordCountResults.txt', 'w', encoding="utf-8") as result_file:
            total_count = 0
            for word, count in results.items():
                result_file.write(f"{word}: {count}\n")
                total_count += count
            result_file.write(f"\nGrand Total: {total_count}\n")
            result_file.write(f"\nTime elapsed: {elapsed_time:.2f} seconds\n")
    except OSError as error:
        print(f"Error writing results: {error}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py <file_with_data.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    start_time = time.time()
    word_counts = count_words(input_file)
    log_elapsed_time = time.time() - start_time

    for log_word, log_count in word_counts.items():
        print(f"{log_word}: {log_count}")
    print(f"\nGrand Total: {sum(word_counts.values())}")
    print(f"\nElapsed time: {log_elapsed_time:.4f} seconds")

    write_results(word_counts, log_elapsed_time)
