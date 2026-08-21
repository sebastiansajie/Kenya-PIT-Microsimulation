# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 07:37:24 2026

@author: ssj34
"""

import pandas as pd
from stata_python import *

PATH = "C:/Users/ssj34/Documents/OneDrive/Other Missions and Projects/IMF Missions/Kenya/Kenya Tax Data/Kenya CIT Model/"

df_cit = pd.read_excel(
    PATH+"CITModel2024_final_r.xlsm",
    sheet_name="Database",
    engine="openpyxl"
)

# Overall summary
print(df_cit["STATION_NAME"].describe())

# Frequency and percentage for every station, including missing values
station_summary = (
    df_cit["STATION_NAME"]
    .fillna("Missing")
    .value_counts(dropna=False)
    .rename_axis("STATION_NAME")
    .reset_index(name="count")
)

station_summary["percentage"] = (
    station_summary["count"] / len(df_cit) * 100
).round(2)

print(station_summary)


df_cit1 = df_cit[df_cit['STATION_NAME']!="PUBLIC SECTOR DIVISION"]
df_cit1= df_cit1.reset_index(drop=True)

df_weight = df_cit1[['TAX_PAYER_ID']].copy()

df_weight['WT2024'] = 1
df_weight['WT2025'] = 1

df_weight['WT2026'] = df_weight['WT2025']
df_weight['WT2027'] = df_weight['WT2025']
df_weight['WT2028'] = df_weight['WT2025']
df_weight['WT2029'] = df_weight['WT2025']
df_weight['WT2030'] = df_weight['WT2025']
df_weight['WT2031'] = df_weight['WT2025']
df_weight['WT2032'] = df_weight['WT2025']

df_weight.drop(columns=['TAX_PAYER_ID'])


df_weight.to_csv('taxcalc/cit_weights_kenya_2024.csv', index=False)


df_cit1 = df_cit1.rename(columns={'TAX_PAYER_ID':'id_n'})
df_cit1['Year'] = 2024
df_cit1.to_csv("taxcalc/cit_kenya_2024_big.csv")

df_cit2 = df_cit1[['id_n', 'Year', 'ADJST_TAXABLE_INCOME_M_9']].copy()

df_cit2.to_csv("taxcalc/cit_kenya_2024.csv")

df_cit_policy = pd.read_excel(
    PATH+"CITModel2024_final_r.xlsm",
    sheet_name="Dashboard",
    engine="openpyxl"
)

df_cit_policy.to_csv("taxcalc/cit_kenya_policy.csv")
