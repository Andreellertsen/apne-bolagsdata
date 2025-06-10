# Öppna bolagsdata

## Quickstart

If you want to reuse [Bolagsverket's High Value Datasets](https://bolagsverket.se/apierochoppnadata/nedladdningsbarafiler.2517.html), the most straightforward way is:

```python
import pandas as pd

scb_data = pd.read_csv(
    "https://vardefulla-datamangder.bolagsverket.se/scb/scb_bulkfil.zip",
    sep="\t",
    encoding="ISO-8859-1",
    low_memory=False,
    compression="zip",
)

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
```

If you need to reuse the data often, I recommend to save and unzip it and load it locally.

You can also check out the data I published on HuggingFace ([scb](https://huggingface.co/datasets/PierreMesure/oppna-bolagsdata-scb), [bolagsverket](https://huggingface.co/datasets/PierreMesure/oppna-bolagsdata-bolagsverket)) but I do not guarantee its freshness.

## License

This code is licensed under AGPLv3. Regarding the data, ask the public agencies. The EU doesn't allow them to use a license more restrictive than CC-BY-4.0 so it's fair to assume that attribution is sufficient.

## Why this little project?

In February 2025, Bolagsverket finally made the Swedish company register free of charge. This is the consequence of the EU directive for High Value Datasets (HVD), which was announced in 2019. Several actors of the Swedish public sector dragged their feet as long as possible (looking at you, Lantmäteriet, Bolagsverket, Regeringskansliet) but they couldn't delay it any longer and we are finally getting the most interesting datasets in 2025.

That being said, Bolagsverket didn't seem so keen to release its data according to open data best practices. So they put their APIs behind a cumbersome authentication process (requiring an account, a secret and a token...). And while it seems that they were also forced to release it as a downloadable file, they apparently didn't have any resource left to make sure these files are in a format that's easy to reuse.

I personally spent a little bit of time to find the best way to work with these files so I thought I would publish my code so others can benefit from it.