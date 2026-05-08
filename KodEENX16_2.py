import zipfile as zip
import os
import pandas as pd
from io import StringIO


def extract_files(zipfilename):
    files = {}
    with zip.ZipFile(zipfilename, 'r') as content:
        for doc in content.namelist():
            filename = os.path.basename(doc)
            files[filename] = content.read(doc).decode("utf-8")
    return files

# Läs in alla filer från zip-filen
data = extract_files('CISS_2024_CSV_files.zip')



######## CRASH.csv ########

# ----- EVENTS & VEHICLES -----
# Läs in CRASH.csv och filtrera fram CASEID där: EVENTS = 1 och VEHICLES = 1
df = pd.read_csv(StringIO(data["CRASH.csv"]))
final_df = df[(df["EVENTS"] == 1) & (df["VEHICLES"] == 1)][["CASEID"]]

# ----- FUELTYPE -----
# Läs in FUEL.csv och filtrera ut FUELTYPE 1, 2, 4, 11
fuel_df = pd.read_csv(StringIO(data["FUEL.csv"]))

fuel_filtered = fuel_df[fuel_df["FUELTYPE"].isin([1, 2, 4, 11])]
fuel_filtered = fuel_filtered[["CASEID", "FUELTYPE"]]

# Slå ihop med final_df
final_df = final_df.merge(fuel_filtered, on="CASEID", how="inner")



######## GV.csv ########

# Läs in GV.csv (WEATHER, SURFCOND, VIN & DVTOTAL)
gv_df = pd.read_csv(StringIO(data["GV.csv"]))

# ----- WEATHER -----
# Filtrera ut WEATHER 1, 2, 3, 4, 5, 6, 8, 9 och 10
weather_df = gv_df[gv_df["WEATHER"].isin([1, 2, 3, 4, 5, 6, 8, 9, 10])][["CASEID", "WEATHER"]]

# Slå ihop WEATHER med final_df
final_df = final_df.merge(weather_df, on="CASEID", how="inner")
final_df["WEATHER"] = final_df["WEATHER"].astype(int)

# ----- SURFCOND -----
# Filtrera ut SURFCOND 1, 2, 3, 4, 5, 6 och 8
surface_df = gv_df[gv_df["SURFCOND"].isin([1, 2, 3, 4, 5, 6, 8])][["CASEID", "SURFCOND"]]

# Slå ihop SURFCOND med final_df
final_df = final_df.merge(surface_df, on="CASEID", how="inner")
final_df["SURFCOND"] = final_df["SURFCOND"].astype(int)

# ----- VIN -----
# Behåll bara VIN och CASEID kopia
vin_df = gv_df[["CASEID", "VIN"]].copy()

# Och om det står massa 9:or istället för VIN, sätt 0
vin_df["VIN"] = vin_df["VIN"].replace(r"^(|0|9+|nan)$", "0", regex=True)

# Slå ihop VIN med final_df och fyll saknade värden med 0
final_df = final_df.merge(vin_df, on="CASEID", how="left")
final_df["VIN"] = final_df["VIN"].fillna("0")

# ----- DVTOTAL -----
# Hämta DVTOTAL ur GV.csv
dv_df = gv_df[["CASEID", "DVTOTAL"]]

# Slå ihop DVTOTAL med final_df
final_df = final_df.merge(dv_df, on="CASEID", how="left")

# Sätt DVTOTAL = 999 där värde saknas
final_df["DVTOTAL"] = final_df["DVTOTAL"].fillna(999).astype(int)

# ----- ROLLOVER -----
# Behåll bara ROLLTYPE och CASEID kopia
roll_df = gv_df[["CASEID", "ROLLTYPE"]].copy()

# Skapa ny variabel
roll_df["ROLLOVER"] = 0

# Rollover = 2, ingen rollover = 1, okänt = 0
roll_df.loc[roll_df["ROLLTYPE"].isin([1, 2, 9]), "ROLLOVER"] = 2
roll_df.loc[roll_df["ROLLTYPE"] == 0, "ROLLOVER"] = 1
roll_df.loc[roll_df["ROLLTYPE"].isin([7]), "ROLLOVER"] = 0

# Slå ihop med final_df, fyll i 0 där data saknas 
final_df = final_df.merge(roll_df[["CASEID", "ROLLOVER"]], on="CASEID", how="left")
final_df["ROLLOVER"] = final_df["ROLLOVER"].fillna(0).astype(int)

# ----- SPEEDLIMIT -----
speed_df = gv_df[["CASEID", "SPEEDLIMIT"]].copy()

# Om värde saknas i filen, sätt 999
speed_df["SPEEDLIMIT"] = speed_df["SPEEDLIMIT"].fillna(999)

# Slå ihop med final_df, fyll saknade värden med 999
final_df = final_df.merge(speed_df, on="CASEID", how="left")
final_df["SPEEDLIMIT"] = final_df["SPEEDLIMIT"].fillna(999).astype(int)

# ----- BODYTYPE -----
bodytype_df = gv_df[["CASEID", "BODYTYPE"]].copy()

# 1 = personbil
bodytype_df.loc[bodytype_df["BODYTYPE"].isin([1,2,3,4,5,6,7,8]), "BODYTYPE"] = 1

# 2 = SUV
bodytype_df.loc[bodytype_df["BODYTYPE"].isin([14,15,16,19]), "BODYTYPE"] = 2

# 3 = pickup / light truck
bodytype_df.loc[bodytype_df["BODYTYPE"].isin([10,32,33,34,39,45,48]), "BODYTYPE"] = 3

# 4 = van / minivan
bodytype_df.loc[bodytype_df["BODYTYPE"].isin([20,21,22,28,29]), "BODYTYPE"] = 4

# Slå ihop (tar bara med relevanta)
final_df = final_df.merge(bodytype_df[bodytype_df["BODYTYPE"] != 0][["CASEID", "BODYTYPE"]], on="CASEID", how="inner")



######## NONMOTORIST.csv ########

# ----- NONMOTORIST -----
# Läs in NONMOTORIST.csv
nonmotor_df = pd.read_csv(StringIO(data["NONMOTORIST.csv"]))

# Gör CASEID till sträng för att matcha final_df - aningen oklart varför detta behövs, men koden kraschar galet utan...????!??!??!?
nonmotor_df["CASEID"] = nonmotor_df["CASEID"].astype(str)
final_df["CASEID"] = final_df["CASEID"].astype(str)

# Ta bort alla CASEID som finns i NONMOTORIST.csv
final_df = final_df[~final_df["CASEID"].isin(nonmotor_df["CASEID"])]



######## OCC.csv ########

# Läs in OCC.csv (PASSENGERS & BELTED_PASSENGERS)
occ_df = pd.read_csv(StringIO(data["OCC.csv"]))

# Gör CASEID till sträng för att matcha final_df
occ_df["CASEID"] = occ_df["CASEID"].astype(str)

# ----- PASSENGERS -----
# Gruppera på CASEID, räkna antal rader i varje grupp, gör till df med namn PASSENGERS
grouped = occ_df.groupby("CASEID")
occ_counts = grouped.size().reset_index(name="PASSENGERS")

# Slå ihop med final_df och fyll saknade värden med 0
final_df = final_df.merge(occ_counts, on="CASEID", how="left")

# Sätt PASSENGERS = 0 där värde saknas
final_df["PASSENGERS"] = final_df["PASSENGERS"].fillna(0).astype(int)

# ----- BELTED_PASSENGERS -----
# BELTUSE-värden som räknas som bältade
belted_values = [1, 2, 3, 4, 5, 8, 12, 13, 14, 15, 18]

# Indikator: 1 = bältad, 0 = ej bältad
occ_df["BELTED"] = occ_df["BELTUSE"].isin(belted_values).astype(int)

# Summera antal bältade personer per CASEID
belt_counts = occ_df.groupby("CASEID")["BELTED"].sum().reset_index(name="BELTED_PASSENGERS")

# Slå ihop med final_df
final_df = final_df.merge(belt_counts, on="CASEID", how="left")

# Sätt BELTED_PASSENGERS = 99 där värde saknas
final_df["BELTED_PASSENGERS"] = final_df["BELTED_PASSENGERS"].fillna(99).astype(int)



######## EVENT.csv ########

# Läs in EVENT.csv + gör CASEID till str för att matcha final_df
event_df = pd.read_csv(StringIO(data["EVENT.csv"]))
event_df["CASEID"] = event_df["CASEID"].astype(str)

# ----- GAD1 -----
# Behåll endast CASEID och GAD1
gad1_df = event_df[["CASEID", "GAD1"]]

# Slå ihop med final_df
final_df = final_df.merge(gad1_df, on="CASEID", how="left")

# Sätt GAD1 = "9" där värde saknas
final_df["GAD1"] = final_df["GAD1"].fillna("9")



######## AIRBAG.csv ########

# ----- AIRBAG -----
# Läs in AIRBAG.csv + gör CASEID till str för att matcha final_df
airbag_df = pd.read_csv(StringIO(data["AIRBAG.csv"]))
airbag_df["CASEID"] = airbag_df["CASEID"].astype(str)

# Skapa ny kolumn som sammanfattar airbag-status per rad
airbag_df["AIRBAG_DEPLOYED"] = 0

# AIRBAG_DEPLOYED = 1 om airbag utlöstes, 2 om den inte utlöstes och 0 om det är okänt
airbag_df.loc[airbag_df["BAGDEPLOY"].isin([1, 2, 3, 4]), "AIRBAG_DEPLOYED"] = 1
airbag_df.loc[airbag_df["BAGDEPLOY"].isin([79, 99]), "AIRBAG_DEPLOYED"] = 0
airbag_df.loc[airbag_df["BAGDEPLOY"].isin([7, 70]), "AIRBAG_DEPLOYED"] = 2

# Kan finnas flera rader per CASEID (flera airbags), reducerar till en rad per CASEID
# 1 vinner över 2, som vinner över 0
airbag_case = airbag_df.groupby("CASEID")["AIRBAG_DEPLOYED"].apply(
    lambda x: 1 if (x == 1).any() else (2 if (x == 2).any() else 0)
).reset_index()

# Slå ihop med final_df och fyll saknade värden med 0 
final_df = final_df.merge(airbag_case, on="CASEID", how="left")
final_df["AIRBAG_DEPLOYED"] = final_df["AIRBAG_DEPLOYED"].fillna(0).astype(int)



######## FIRE.csv ########

# ----- FIRE -----
# Läs in FIRE.csv + gör CASEID till str för att matcha final_df
fire_df = pd.read_csv(StringIO(data["FIRE.csv"]))
fire_df["CASEID"] = fire_df["CASEID"].astype(str)
final_df["CASEID"] = final_df["CASEID"].astype(str)

# Behåll bara CASEID och FIRE
fire_filtered = fire_df[["CASEID", "FIRE"]]

# Slå ihop med final_df
final_df = final_df.merge(fire_filtered, on="CASEID", how="left")

# Omkodning
mapping = {
    0: 1,  # no fire
    1: 2,  # fire
    2: 2,  # fire
    9: 9   # unknown
}

# Applicera omkodningen och fyll i saknade värden med 9
final_df["FIRE"] = final_df["FIRE"].map(mapping)
final_df["FIRE"] = final_df["FIRE"].fillna(9).astype(int)



######## SPARA RESULTAT ########
final_df.to_csv("FINAL.csv", index=False)
