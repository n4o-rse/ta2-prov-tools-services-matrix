import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS, FOAF, XSD
import os

# === Konfiguration ===
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(script_dir, "Matrix_v1.csv")
jsonld_path = os.path.join(script_dir, "metadata.jsonld")
ttl_file = csv_file.replace(".csv", ".ttl")

# === Namespaces ===
BASE = Namespace("https://w3id.org/n4o-metadata/prov-matrix/")
OBJECTCORE = Namespace("https://w3id.org/objectcoreont/")
OCMDP = Namespace("http://www.w3id.org/objectcore/terminology/")

# === Typen-Mapping ===
type_uri_mapping = {
    "NetzwerkeServices": "https://w3id.org/objectcoreont/F-R7HUAW",
    "RechercheRessourcen": "https://w3id.org/objectcoreont/F-MGQGXG",
    "DigitaleAnwendungen": "https://w3id.org/objectcoreont/F-YBBA5L",
    "Empfehlungen": "https://w3id.org/objectcoreont/F-E5JM9H"
}

# === Kategorien-Mapping ===
category_mapping = {
    "KulturSammlungsgutKolonialeKontexte": "IP5W9R",
    "NsverfolgungsbedingtEntzogenesKulturgut": "A01ISV",
    "KulturgutentziehungenSBZDDR": "D1ZG69",
    "KriegsbedingtVerlagertesKulturgut": "IVETAX",
    "SecretSacredObjects": "Z5V1LB",
    "HumanRemains": "SZMZE4",
    "NaturkundeNaturwissenschaft": "A0VF7A"
}
OCMDP_PREFIX = "http://www.w3id.org/objectcore/terminology/"

# === RDF-Graph initialisieren ===
g = Graph()
g.bind("dct", DCTERMS)
g.bind("foaf", FOAF)
g.bind("rdfs", RDFS)
g.bind("rdf", RDF)
g.bind("base", BASE)
g.bind("objectcore", OBJECTCORE)
g.bind("ocmdp", OCMDP)

# === Metadaten aus metadata.jsonld in Graph einfügen ===
g.parse(jsonld_path, format="json-ld")

# === CSV einlesen ===
df = pd.read_csv(csv_file, sep=",", quotechar='"', dtype=str).fillna("")

# === Verarbeitung jeder Zeile ===
for i, row in df.iterrows():
    res_uri = URIRef(BASE + str(row["ID"]))
    
    # Basis-Typ
    g.add((res_uri, RDF.type, URIRef("http://www.w3.org/ns/dcat#Resource")))

    # Typen aus Mapping
    for type_col, type_uri in type_uri_mapping.items():
        if row.get(type_col, "").strip().lower() == "x":
            g.add((res_uri, RDF.type, URIRef(type_uri)))

    # Kategorien aus Mapping
    for cat_col, ocmdp_id in category_mapping.items():
        if row.get(cat_col, "").strip().lower() == "x":
            g.add((res_uri, DCTERMS.subject, URIRef(OCMDP_PREFIX + ocmdp_id)))

# === Turtle-Datei schreiben ===
g.serialize(destination=ttl_file, format="turtle")
print(f"✅ RDF Turtle-Datei erstellt: {ttl_file}")
