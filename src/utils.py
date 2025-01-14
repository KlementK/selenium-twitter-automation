# src/utils.py
import logging
import csv
import json


def save_to_csv(data, output_file="tweets.csv"):
    """
    Save a list of dictionaries (tweets) to a CSV file.
    """
    if not data:
        logging.warning("No data to save to CSV.")
        return

    keys = list(data[0].keys())
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    logging.info(f"Data saved to {output_file} (CSV).")


def save_to_json(data, output_file="tweets.json"):
    """
    Save a list of dictionaries (tweets) to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logging.info(f"Data saved to {output_file} (JSON).")
