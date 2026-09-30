# -*- coding: utf-8 -*-
__author__ = "Mathias Strunck Gundersen"
__email__ = "magun9077@nmbu.no"


import json # for å lage .json filer
import yaml # for å lese yml filer
import pandas as pd #for å lese csv og excel filer
from pathlib import Path

# setter opp paths for å kunne navigere til filene
yml_file = Path(__file__).with_name("config.yml")
excel_file = Path(__file__).with_name("sensors.xlsx")
csv_file = Path(__file__).with_name("calibrations.csv")

"""endret output_file i yml fil til en annen mappe enn venv"""

def main():
    # 1. Les innstillinger 
    with open(yml_file, "r") as f:
        config = yaml.safe_load(f)

    max_days = config["max_days_since_calibration"] # setter max dager (180)
    output_file = config["output_file"] 

    # 2. Les data
    sensors = pd.read_excel(excel_file)        # sensor_id, lab_room, owner
    calibrations = pd.read_csv(csv_file)  # sensor_id, days_since_calibration

    # 3. Slå sammen på sensor_id
    merged = sensors.merge(calibrations, on="sensor_id", how="inner")

    # 4. Filtrer: kun sensorer over grensen 
    overdue = merged[merged["days_since_calibration"] > max_days]

    # 5. Eksportere til json 
    columns = ["sensor_id", "lab_room", "owner", "days_since_calibration"]
    records = overdue[columns].to_dict(orient="records")

    # int() konverterer numpy-typer til vanlige Python-tall 
    # json.dump kan ikke serialisere numpy direkte)
    for rec in records:
        rec["days_since_calibration"] = int(rec["days_since_calibration"])

    with open(output_file, "w") as Jfile:
        json.dump(records, Jfile, indent=2) #legger records listen inn i en json fil
        #indent = 2 gjør det lettere å lese

    print(f"Grense: {max_days} dager")
    print(f"{len(records)} forfalt sensor skrevet til {output_file}")


if __name__ == "__main__":
    main()