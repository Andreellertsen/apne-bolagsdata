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
bv_data = pd.read_csv(
    "https://vardefulla-datamangder.bolagsverket.se/bolagsverket/bolagsverket_bulkfil.zip",
    sep=";",
    encoding="utf-8",
    low_memory=False,
    quotechar='"',
    escapechar="\\",
    on_bad_lines="warn",
    compression="zip",
)

# Remove sole traders and personal data
scb_data = scb_data[scb_data["PeOrgNr"] < 190000000000]
scb_data.drop("COAdress", axis=1, inplace=True)

# Add a column to filter sole traders (enskilda firmor)
# This is unnecessary since we remove them
# scb_data["enskildfirma"] = scb_data["PeOrgNr"] > 190000000000

# Remove sole traders
bv_data = bv_data[
    ~bv_data["organisationsidentitet"].str.contains("\\$PERSON-IDORG", regex=True)
]

# Add a column to filter sole traders (enskilda firmor)
# This is unnecessary since we remove them
# bv_data["enskildfirma"] = bv_data["organisationsidentitet"].str.contains(
#     "\\$PERSON-IDORG", regex=True
# )
# bv_data["organisationsidentitet"] = bv_data["organisationsidentitet"].str.replace(
#     "$PERSON-IDORG", ""
# )


# Clean columns
bv_data["organisationsidentitet"] = bv_data["organisationsidentitet"].str.replace(
    "$ORGNR-IDORG", ""
)
bv_data["organisationsnamn"] = (
    bv_data["organisationsnamn"].str.split("$FORETAGSNAMN").str[0]
)
bv_data["postadress"] = (
    bv_data["postadress"]
    .str.replace("$SE-LAND", "")
    .str.replace("$$", "\n")
    .str.replace("$", "\n")
)

print("Converting to datasets...")
scb_dataset = Dataset.from_pandas(scb_data)
bv_dataset = Dataset.from_pandas(bv_data)

print("Uploading to HuggingFace...")
scb_dataset.push_to_hub(
    commit_message="Update the data", repo_id="PierreMesure/oppna-bolagsdata-scb"
)
bv_dataset.push_to_hub(
    commit_message="Update the data",
    repo_id="PierreMesure/oppna-bolagsdata-bolagsverket",
)

print("Done!")
