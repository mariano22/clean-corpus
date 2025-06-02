import argparse
from datasets import Dataset
import clean_corpus as cc  # Import the clean_corpus module

from .utils import load_ds  # Import load_ds from utils

def load_webz_dataset(ds_name):
    dataset = Dataset.from_generator(load_ds, gen_kwargs={'ds_name':ds_name})
    return dataset

def load_ds_from_disk(ds_path):
    dataset = Dataset.load_from_disk(ds_path)
    return dataset

def fill_gopher_verdict(ds):
    # Logic to fill gopher_verdict field
    pass  # Replace with actual implementation

def fill_en_proba(ds):
    # Logic to fill en_proba field
    pass  # Replace with actual implementation

def main():
    parser = argparse.ArgumentParser(description="Clean and preprocess text dataset.")
    
    # Mutually exclusive group for loading datasets
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--load_webz_dataset", type=str, help="Load a dataset by name.")
    group.add_argument("--load_ds_from_disk", type=str, help="Load a dataset from disk.")
    
    args = parser.parse_args()

    if args.load_webz_dataset:
        ds = load_webz_dataset(args.load_webz_dataset)
        print(f"Loaded webz dataset: {args.load_webz_dataset}")

    if args.load_ds_from_disk:
        ds = load_ds_from_disk(args.load_ds_from_disk)
        print(f"Loaded dataset from disk: {args.load_ds_from_disk}")

    if 'ds' in locals():
        fill_gopher_verdict(ds)
        fill_en_proba(ds)