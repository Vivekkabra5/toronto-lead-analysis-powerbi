"""Rebuild data/fsa_lookup.csv (Toronto FSA centroids) from the GeoNames postal-code dump.

Source: https://download.geonames.org/export/zip/CA.zip (CC BY 4.0).
Usage:  python scripts/build_fsa_lookup.py
"""
import csv
import io
import pathlib
import urllib.request
import zipfile

OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "fsa_lookup.csv"

raw = urllib.request.urlopen("https://download.geonames.org/export/zip/CA.zip").read()
text = zipfile.ZipFile(io.BytesIO(raw)).read("CA.txt").decode("utf-8")

rows = []
for line in text.splitlines():
    f = line.split("\t")
    if f[1].startswith("M"):  # Toronto FSAs start with M
        name = f[2]  # e.g. "East Toronto (The Beaches)"
        area = name.split(" (")[0]
        hoods = name[len(area):].strip(" ()") or area
        rows.append([f[1], area, hoods, f[9], f[10]])

with open(OUT, "w", newline="", encoding="utf-8") as o:
    w = csv.writer(o)
    w.writerow(["FSA", "Area", "Neighbourhoods", "Latitude", "Longitude"])
    w.writerows(rows)
print(f"wrote {len(rows)} FSAs to {OUT}")
