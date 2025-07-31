import pandas as pd
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(script_dir, "Matrix_v1.csv")

# CSV einlesen mit "," als Trennzeichen und doppelten Anführungszeichen
df = pd.read_csv(csv_file, sep=",", quotechar='"', dtype=str).fillna("")

# Definition: Textfelder
text_fields = ["ID", "Bezeichnung", "Beschreibung", "URL"]

# Mapping der Spalten zu OCMDP-IDs
column_to_ocmdp = {
    "NsverfolgungsbedingtEntzogenesKulturgut": "A01ISV",
    "KulturSammlungsgutKolonialeKontexte": "IP5W9R",
    "KulturgutentziehungenSBZDDR": "D1ZG69",
    "KriegsbedingtVerlagertesKulturgut": "IVETAX",
    "SecretSacredObjects": "Z5V1LB",
    "HumanRemains": "SZMZE4",
    "NaturkundeNaturwissenschaft": "A0VF7A",
    "NetzwerkeServices": "WXJBI5",
    "DigitaleAnwendungen": "PSEBRV",
    "Empfehlungen": "UOVWQQ",
    "RechercheRessourcen": "UQBLZP"
}

# OCMDP-URI-Präfix
prefix = "http://www.w3id.org/objectcore/terminology/"

# Gruppierung: Was ist Kategorie, was ist Typ
category_keys = {
    "KulturSammlungsgutKolonialeKontexte",
    "NsverfolgungsbedingtEntzogenesKulturgut",
    "KulturgutentziehungenSBZDDR",
    "KriegsbedingtVerlagertesKulturgut",
    "HumanRemains",
    "SecretSacredObjects",
    "NaturkundeNaturwissenschaft"
}

type_keys = {
    "NetzwerkeServices",
    "DigitaleAnwendungen",
    "Empfehlungen",
    "RechercheRessourcen"
}

# Alle Booleschen Felder: alle außer den Textfeldern
bool_fields = [col for col in df.columns if col not in text_fields]

# === JSON 1: Mit Boolean-Feldern ===
records = []
for i, (_, row) in enumerate(df.iterrows(), start=1):
    obj = {
        "internalID": i,
        **{field: row[field] for field in text_fields},
        **{field: row[field].strip().lower() == "x" for field in bool_fields}
    }
    records.append(obj)

# === JSON 2: Mit category/type URIs ===
extended_records = []
for i, row in enumerate(df.itertuples(index=False), start=1):
    base = {
        "internalID": i,
        **{field: getattr(row, field) for field in text_fields}
    }

    categories = []
    types = []

    for col, ocmdp_id in column_to_ocmdp.items():
        val = getattr(row, col, "").strip().lower()
        if val == "x":
            uri = prefix + ocmdp_id
            if col in category_keys:
                categories.append(uri)
            elif col in type_keys:
                types.append(uri)

    if categories:
        base["category"] = categories
    if types:
        base["type"] = types

    extended_records.append(base)

# === Dateien schreiben ===
base_name = os.path.splitext(csv_file)[0]

with open(base_name + ".json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

with open(base_name + "_extended.json", "w", encoding="utf-8") as f:
    json.dump(extended_records, f, indent=2, ensure_ascii=False)

print("✅ JSON-Dateien erfolgreich erstellt:")
print(f"- {base_name}.json (mit Booleans)")
print(f"- {base_name}_extended.json (mit category/type URIs)")
