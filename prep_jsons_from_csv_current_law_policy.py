# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 16:39:02 2025

@author: ssj34
"""

import pandas as pd
import json

def checknan(value):
    if (value=="nan"):
        value=""
    return value

def parse_number_or_reference(value):
    """
    Convert numbers to int/float and policy-parameter references to
    underscore-prefixed strings.
    """
    if pd.isna(value):
        return None

    text = str(value).strip()

    if text == "":
        return None

    # Integer values such as 0 and 1
    try:
        if "." not in text and "e" not in text.lower():
            return int(text)
    except ValueError:
        pass

    # Decimal and scientific-notation values
    try:
        return float(text)
    except ValueError:
        pass

    # Any remaining range value is a policy-parameter reference.
    return "_" + text.lstrip("_")
    
df = pd.read_csv("current_law_policy_input_pit.csv")
final_json = {}
cols = list(df.columns)
for idx, row in df.iterrows():
    csv_field_name = str(row["field_name"]).strip()
    field_name = "_" + csv_field_name.lstrip("_")
    print(field_name)
    item = {}
    item['long_name'] = str(row['long_name'])
    item['description'] = str(row['description'])
    item['itr_ref'] = str(row['itr_ref'])
    item['notes'] = checknan(str(row['notes']))
    item['row_var'] = str(row['row_var'])
    item['row_label'] = [str(int(row['row_label']))]
    item['start_year'] = int(row['start_year'])
    item['cpi_inflatable'] = row['cpi_inflatable']
    item['cpi_inflated'] = row['cpi_inflated']
    item['col_var'] = checknan(str(row['col_var']))
    if (field_name.find('elasticity')!=-1):
        item['col_label'] = ["bracket1", "bracket2", "bracket3"]
        if (field_name.find('threshold')!=-1):
            item['value'] = [[100000, 1000000, 9e99]]
        elif (field_name.find('value')!=-1):
            if (field_name.find('food')!=-1):
                item['value'] = [[0.0, 0.0, 0.0]]
            else:
                item['value'] = [[0.0, 0.0, 0.0]]
    else:
        item['col_label'] = checknan(str(row['col_label']))
        item['value'] = [(row['value'])]
    item['boolean_value'] = row['boolean_value']
    item['integer_value'] = row['integer_value']
    item["range"] = {
        "min": parse_number_or_reference(row["min"]),
        "max": parse_number_or_reference(row["max"])
    }
    item['out_of_range_minmsg'] = checknan(str(row['out_of_range_minmsg']))
    item['out_of_range_maxmsg'] = checknan(str(row['out_of_range_maxmsg']))
    item['out_of_range_action'] = str(row['out_of_range_action'])
    final_json[field_name]=item

with open('taxcalc/current_law_policy_pit_kenya.json', 'w') as f:
    json.dump(final_json, f, indent=4)
    
print(f"JSON successfully written {final_json}")

