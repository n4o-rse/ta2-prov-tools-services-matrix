import pandas as pd
import json
import os

# Pfad zur CSV-Datei im gleichen Ordner wie dieses Skript
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(script_dir, "Matrix_v1.csv")

# CSV einlesen mit Komma als Separator und doppelten Anführungszeichen
df = pd.read_csv(csv_file, sep=",", quotechar='"', dtype=str).fillna("")

# Textfelder definieren
text_fields = ["ID", "Bezeichnung", "Beschreibung", "URL"]
bool_fields = [col for col in df.columns if col not in text_fields]

# JSON-Daten erzeugen mit zusätzlichem internalID (beginnend bei 1)
records = []
for i, (_, row) in enumerate(df.iterrows(), start=1):
    obj = {
        "internalID": i,
        **{field: row[field] for field in text_fields},
        **{field: row[field].strip().lower() == "x" for field in bool_fields}
    }
    records.append(obj)

# JSON-Dateiname ableiten
json_file = os.path.splitext(csv_file)[0] + ".json"

# JSON-Datei schreiben
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print(f"✅ JSON-Datei mit 'internalID' erstellt: {json_file}")
