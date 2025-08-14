import pandas as pd
import duckdb

# ----------------------------------------------------
# 1. Last ned og les SCB-data
# ----------------------------------------------------
print("Downloading SCB's data...")
scb_data = pd.read_csv(
    "https://vardefulla-datamangder.bolagsverket.se/scb/scb_bulkfil.zip",
    sep="\t",
    encoding="ISO-8859-1",
    low_memory=False,
    compression="zip",
)

# ----------------------------------------------------
# 2. Last ned og les Bolagsverket-data
# ----------------------------------------------------
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

# ----------------------------------------------------
# 3. Rens SCB-data
# ----------------------------------------------------
# Fjern personnummer (enskild firma) og c/o-adresse
scb_data = scb_data[scb_data["PeOrgNr"] < 190000000000]
scb_data.drop("COAdress", axis=1, inplace=True)

# ----------------------------------------------------
# 4. Rens Bolagsverket-data
# ----------------------------------------------------
# Fjern person-IDORGer
bv_data = bv_data[
    ~bv_data["organisationsidentitet"].str.contains("\\$PERSON-IDORG", regex=True)
]

# Fjern tekniske markører fra kolonnene
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

# ----------------------------------------------------
# 5. Lagre til DuckDB
# ----------------------------------------------------
print("Saving to DuckDB...")
con = duckdb.connect("bolagsdata.duckdb")  # Lager/åpner databasefil

# Lag tabeller
con.execute("CREATE OR REPLACE TABLE scb AS SELECT * FROM scb_data")
con.execute("CREATE OR REPLACE TABLE bolagsverket AS SELECT * FROM bv_data")

# Bekreft lagring
print("Data saved to 'bolagsdata.duckdb'")
print("Tables in DB:", con.execute("SHOW TABLES").fetchall())

con.close()
