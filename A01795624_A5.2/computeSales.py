"""
Computes the total cost of sales based on a price catalogue and sales record.
"""
import json
import sys
import time


def load_json_file(file_path):
    """
    Loads a JSON data from a file.
    Handles file not found and JSON decoding errors.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' contains invalid JSON.")
    return None


def build_price_catalogue(catalog_data):
    """
    Builds a price dictionary from catalog data.
    """
    return {item['title']: item['price'] for item in catalog_data}


def compute_total_sales(price_catalogue, sales_record):
    """
    Computes total cost of all sales based on price catalogue.
    """
    total_cost = 0
    errors = []

    for sale in sales_record:
        product = sale.get('Product')
        quantity = sale.get('Quantity')

        if product is None or quantity is None:
            errors.append("Invalid record: Missing product or quantity.")
            continue

        if product not in price_catalogue:
            errors.append(f"Error: Product '{product}' not found in list.")
            continue

        try:
            price = float(price_catalogue[product])
            total_cost += price * int(quantity)
        except ValueError:
            errors.append(f"Error: Invalid price or quantity for '{product}'.")

    return total_cost, errors


def save_results(total_cost, errors, execution_time):
    """
    Save results to SalesResults.txt and print output.
    """
    output = [
        f"Total Sales Cost: ${total_cost:.2f}",
        f"Execution Time: {execution_time:.4f} seconds",
        "Errors:"
    ]
    output.extend(errors if errors else ["None"])

    # Print results to console
    print("\n".join(output))

    # Save results to file
    with open("SalesResults.txt", 'w', encoding='utf-8') as file:
        file.write("\n".join(output) + "\n")


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("""Usage:
            python computeSales.py priceCatalogue.json salesRecord.json""")
        sys.exit(1)

    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    # We first load the two JSON's files
    log_catalog_data = load_json_file(price_catalogue_file)
    sales_data = load_json_file(sales_record_file)

    if log_catalog_data is None or sales_data is None:
        sys.exit(1)

    # Then we build price catalogue from catalog data
    log_price_catalogue = build_price_catalogue(log_catalog_data)

    # After, we compute the total sales
    start_time = time.time()
    log_total_cost, log_errors = compute_total_sales(
        log_price_catalogue,
        sales_data
    )
    log_execution_time = time.time() - start_time

    # Lastly, we save and display results
    save_results(log_total_cost, log_errors, log_execution_time)
