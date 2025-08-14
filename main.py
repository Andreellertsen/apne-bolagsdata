import pandas as pd
import duckdb
import requests
from io import BytesIO
from zipfile import ZipFile

def read_zip_csv(url):
    response = requests.get(url)
    with ZipFile(BytesIO(response.content)) as zf:
        csv_name = zf.namelist()[0]  # take the first file
        with zf.open(csv_name) as f:
            # Use sep=None and engine='python' to auto-detect separator
            # on_bad_lines='skip' skips rows that break column counts
            return pd.read_csv(f, sep=None, engine='python', encoding='latin-1', on_bad_lines='skip')


# ----------------------------------------------------
# 1. Last ned og les SCB-data
# ----------------------------------------------------
print("Downloading SCB's data...")
scb_data = read_zip_csv(
    "https://vardefulla-datamangder.bolagsverket.se/scb/scb_bulkfil.zip"
)

# ----------------------------------------------------
# 2. Last ned og les Bolagsverket-data
# ----------------------------------------------------
print("Downloading Bolagsverket's data...")
bv_data = read_zip_csv(
    "https://vardefulla-datamangder.bolagsverket.se/bolagsverket/bolagsverket_bulkfil.zip"
)

# ----------------------------------------------------
# 3. Rens SCB-data
# ----------------------------------------------------
scb_data = scb_data[scb_data["PeOrgNr"] < 190000000000]
scb_data.drop("COAdress", axis=1, inplace=True)

# ----------------------------------------------------
# 4. Rens Bolagsverket-data
# ----------------------------------------------------
bv_data = bv_data[~bv_data["organisationsidentitet"].str.contains("\\$PERSON-IDORG", regex=True)]
bv_data["organisationsidentitet"] = bv_data["organisationsidentitet"].str.replace("$ORGNR-IDORG", "", regex=False)
bv_data["organisationsnamn"] = bv_data["organisationsnamn"].str.split("$FORETAGSNAMN").str[0]
bv_data["postadress"] = bv_data["postadress"].str.replace("$SE-LAND", "", regex=False)\
                                               .str.replace("$$", "\n", regex=False)\
                                               .str.replace("$", "\n", regex=False)

# ----------------------------------------------------
# 5. Lagre til DuckDB
# ----------------------------------------------------
print("Saving to DuckDB...")
con = duckdb.connect("bolagsdata.duckdb")
con.execute("CREATE OR REPLACE TABLE scb AS SELECT * FROM scb_data")
con.execute("CREATE OR REPLACE TABLE bolagsverket AS SELECT * FROM bv_data")

print("Data saved to 'bolagsdata.duckdb'")
print("Tables in DB:", con.execute("SHOW TABLES").fetchall())
con.close()
