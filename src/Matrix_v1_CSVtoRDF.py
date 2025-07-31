import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS, FOAF, XSD
import json
import os

# === Konfiguration ===
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(script_dir, "Matrix_v1.csv")
ttl_file = csv_file.replace(".csv", ".ttl")

BASE = Namespace("https://w3id.org/n4o-metadata/prov-matrix/")
OBJECTCORE = Namespace("https://w3id.org/objectcoreont/")
OCMDP = Namespace("http://www.w3id.org/objectcore/terminology/")

# Typen-Mapping
type_uri_mapping = {
    "NetzwerkeServices": "https://w3id.org/objectcoreont/F-R7HUAW",
    "RechercheRessourcen": "https://w3id.org/objectcoreont/F-MGQGXG",
    "DigitaleAnwendungen": "https://w3id.org/objectcoreont/F-YBBA5L",
    "Empfehlungen": "https://w3id.org/objectcoreont/F-E5JM9H"
}

# Kategorien (bleiben erstmal wie zuvor, OCMDP-ID Mapping kann später folgen)
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

# === Graph anlegen ===
g = Graph()
g.bind("dct", DCTERMS)
g.bind("foaf", FOAF)
g.bind("rdfs", RDFS)
g.bind("rdf", RDF)
g.bind("base", BASE)
g.bind("objectcore", OBJECTCORE)
g.bind("ocmdp", OCMDP)

# === CSV einlesen ===
df = pd.read_csv(csv_file, sep=",", quotechar='"', dtype=str).fillna("")

# Textfelder
text_fields = ["ID", "Bezeichnung", "Beschreibung", "URL"]

# === Verarbeitung ===
for i, row in df.iterrows():
    res_uri = URIRef(BASE + str(row["ID"]))
    g.add((res_uri, RDF.type, URIRef("http://www.w3.org/ns/dcat#Resource")))

    # Textfelder hinzufügen
    #g.add((res_uri, DCTERMS.identifier, Literal(row["ID"], datatype=XSD.string)))
    #g.add((res_uri, DCTERMS.title, Literal(row["Bezeichnung"], datatype=XSD.string)))
    #g.add((res_uri, DCTERMS.description, Literal(row["Beschreibung"], datatype=XSD.string)))
    #if row["URL"].strip():
    #    g.add((res_uri, DCTERMS.source, URIRef(row["URL"])))

    # Kategorien
    for cat_col, ocmdp_id in category_mapping.items():
        if row.get(cat_col, "").strip().lower() == "x":
            g.add((res_uri, DCTERMS.subject, URIRef(OCMDP_PREFIX + ocmdp_id)))

    # Typen
    for type_col, type_uri in type_uri_mapping.items():
        if row.get(type_col, "").strip().lower() == "x":
            g.add((res_uri, RDF.type, URIRef(type_uri)))

# === Turtle schreiben ===
g.serialize(destination=ttl_file, format="turtle")
print(f"✅ RDF Turtle-Datei erstellt: {ttl_file}")
