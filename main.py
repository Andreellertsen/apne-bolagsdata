import pandas as pd
from datasets import Dataset, DatasetDict
from huggingface_hub import login

print("Downloading SCB's data...")
scb_data = pd.read_csv(
    "https://vardefulla-datamangder.bolagsverket.se/scb/scb_bulkfil.zip",
    sep="\t",
    encoding="ISO-8859-1",
    low_memory=False,
    compression="zip",
)

print("Downloading Bolagsverket's data...")
bolagsverket_data = pd.read_csv(
    "https://vardefulla-datamangder.bolagsverket.se/bolagsverket/bolagsverket_bulkfil.zip",
    sep=";",
    encoding="utf-8",
    low_memory=False,
    quotechar='"',
    escapechar="\\",
    on_bad_lines="warn",
    compression="zip",
)

print("Converting to datasets...")
scb_dataset = Dataset.from_pandas(scb_data)
bolagsverket_dataset = Dataset.from_pandas(bolagsverket_data)

print("Uploading to HuggingFace...")
scb_dataset.push_to_hub(commit_message="Update the data", repo_id="PierreMesure/oppna-bolagsdata-scb")
bolagsverket_dataset.push_to_hub(commit_message="Update the data", repo_id="PierreMesure/oppna-bolagsdata-bolagsverket")

print("Done!")