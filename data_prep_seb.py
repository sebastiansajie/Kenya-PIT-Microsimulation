import pandas as pd
import numpy as np
from stata_python import * 

df_bus=pd.read_csv("profit_and_loss.csv")
df_bus = df_bus.dropna(subset=['tax_payer_id'])
df_bus = df_bus.drop_duplicates(
    subset=["tax_payer_id"],
    keep="last"
)

df_emp = pd.read_csv("employment_income.csv")
df_emp = df_emp.dropna(subset=['tax_payer_id'])
df_emp = df_emp.drop_duplicates(
    subset=["tax_payer_id"],
    keep="last"
)

df_cgt=pd.read_csv("cgt_pit.csv")
df_cgt = df_cgt.dropna(subset=['tax_payer_id'])
df_cgt_with_summary = (
    df_cgt
    .groupby(['tax_payer_id', 'cgt_type'], as_index=False)
    .agg({
        'diff_being_adjusted_capital_gain': 'sum',
        'capital_gain_tax': 'sum',
        'total_amount_payable':'sum',
        'total_amount_paid':'sum'
    })
)
value_cols = [
    'diff_being_adjusted_capital_gain',
    'capital_gain_tax',
    'total_amount_payable',
    'total_amount_paid'
]
df_cgt_wide = (
    df_cgt_with_summary
    .pivot_table(
        index='tax_payer_id',
        columns='cgt_type',
        values=value_cols,
        aggfunc='sum',
        fill_value=0
    )
)
# Flatten the multi-level column names
df_cgt_wide.columns = [
    f'{cgt_type}_{value}'
    for value, cgt_type in df_cgt_wide.columns
]
# Make tax_payer_id a normal column again
df_cgt_wide = df_cgt_wide.reset_index()

df_with=pd.read_csv("withholding_tax.csv")
df_with = df_with.dropna(subset=['tax_payer_id'])
df_with_summary = (
    df_with
    .groupby(['tax_payer_id'], as_index=False)
    .agg({
        'gross_amount': 'sum',
        'amount_withheld': 'sum'
    })
)

df_rent=pd.read_csv("rental_returns.csv")
df_rent = df_rent.dropna(subset=['tax_payer_id'])
df_rent_summary = (
    df_rent
    .groupby(['tax_payer_id'], as_index=False)
    .agg({
        'tot_rent_income': 'sum',
        'tax_on_rent_income': 'sum',
        'paid':'sum'
    })
)

df = (
    df_bus
    .merge(df_cgt_wide, on='tax_payer_id', how='outer')
    .merge(df_with_summary, on='tax_payer_id', how='outer')
    .merge(df_rent_summary, on='tax_payer_id', how='outer')
)

# Create income-type indicators
df['Employment_Business'] = df['tax_payer_id'].isin(
    df_bus['tax_payer_id'].dropna()
)

df['CGT'] = df['tax_payer_id'].isin(
    df_cgt_wide['tax_payer_id'].dropna()
)

df['Withholding'] = df['tax_payer_id'].isin(
    df_with_summary['tax_payer_id'].dropna()
)

df['Rent'] = df['tax_payer_id'].isin(
    df_rent_summary['tax_payer_id'].dropna()
)

# Count number of income types for each taxpayer
income_cols = ['Employment_Business', 'CGT', 'Withholding', 'Rent']

df['number_of_income_types'] = df[income_cols].sum(axis=1)

df['income_combination'] = df[income_cols].apply(
    lambda x: ' + '.join(x.index[x]),
    axis=1
)

combination_summary = (
    df['income_combination']
    .value_counts()
    .reset_index()
)

combination_summary.columns = [
    'Income_combination',
    'Number_of_taxpayers'
]

combination_summary

df = df.rename(
    columns={
        'gross_amount':'interest_dividend'
        })

income_cols = [
    'tot_emp_income',
    'CGT_1_diff_being_adjusted_capital_gain',
    'CGT_2_diff_being_adjusted_capital_gain',
    'CGT_1P_diff_being_adjusted_capital_gain',
    'interest_dividend',
    'tot_rent_income'
]

# Fill NaN with 0
df[income_cols] = df[income_cols].fillna(0)

# Calculate gross income
df['gross_income'] = df[income_cols].sum(axis=1)

df.to_csv("pit_merged.csv")  

# df_bus=pd.read_csv("profit_and_loss.csv")

# df_bus = df_bus.dropna(subset=['tax_payer_id'])

# df_bus_emp = pd.merge(df_bus,df_emp,on="tax_payer_id",how="outer", indicator=True)

# # Unique taxpayer IDs in each dataset
# bus_ids = set(df_bus['tax_payer_id'].dropna().unique())
# emp_ids = set(df_emp['tax_payer_id'].dropna().unique())

# # Calculate taxpayer groups
# business_only = bus_ids - emp_ids
# employment_only = emp_ids - bus_ids
# both = bus_ids & emp_ids

# summary = pd.DataFrame({
#     'income_category': [
#         'Business income only',
#         'Employment income only',
#         'Both business and employment'
#     ],
#     'number_of_taxpayers': [
#         len(business_only),
#         len(employment_only),
#         len(both)
#     ]
# })

# summary['percentage'] = (
#     summary['number_of_taxpayers']
#     / summary['number_of_taxpayers'].sum()
#     * 100
# ).round(2)

# summary

# df_compare = pd.merge(
#     df_bus,
#     df_emp,
#     on='tax_payer_id',
#     how='inner',
#     suffixes=('_bus', '_emp')
# )

# df_compare['tot_emp_income_match'] = np.isclose(
#     df_compare['tot_emp_income_bus'],
#     df_compare['tot_emp_income_emp'],
#     equal_nan=True
# )

# df_compare['net_taxable_income_match'] = np.isclose(
#     df_compare['net_taxable_income_bus'],
#     df_compare['net_taxable_income_emp'],
#     equal_nan=True
# )

# summary = pd.DataFrame({
#     'Field': [
#         'tot_emp_income',
#         'net_taxable_income'
#     ],
#     'Match': [
#         df_compare['tot_emp_income_match'].sum(),
#         df_compare['net_taxable_income_match'].sum()
#     ],
#     'Do not match': [
#         (~df_compare['tot_emp_income_match']).sum(),
#         (~df_compare['net_taxable_income_match']).sum()
#     ]
# })

# summary


# summary['Total'] = summary['Match'] + summary['Do not match']

# summary['Match_percentage'] = (
#     summary['Match'] / summary['Total'] * 100
# ).round(2)

# summary
