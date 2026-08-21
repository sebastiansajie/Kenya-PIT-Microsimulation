"""
This is a file that allows sampling of a large dataset.
"""
# import sys
# sys.path.insert(0, 'C:/Users/wb305167/OneDrive - WBG/python_latest/Tax-Revenue-Analysis')
# from stata_python import *
import pandas as pd
import numpy as np

pit_df_2025=pd.read_csv('pit_merged.csv')

pit_df_2025=pit_df_2025.sort_values(by=['gross_income'])

pit_df_2025 = pit_df_2025[pit_df_2025['gross_income'] != 0]

pit_df_2025=pit_df_2025.reset_index()

# allocate the data into bins
pit_df_2025['bin'] = pd.qcut(pit_df_2025['gross_income'], 10, labels=False)
pit_df_2025['weight']=1
# bin_ratio is the fraction of the number of records selected in each bin
# 1/10,...1/5, 1/1
bin_ratio=[50,50,50,50,20,20,10,5,2,1]
frames=[]
df={}
for i in range(len(bin_ratio)):
    # find out the size of each bin
    bin_size=len(pit_df_2025[pit_df_2025['bin']==i])//bin_ratio[i]
    # draw a random sample from each bin
    df[i]=pit_df_2025[pit_df_2025['bin']==i].sample(n=bin_size)
    df[i]['weight'] = bin_ratio[i]
    frames=frames+[df[i]]

pit_sample_2025= pd.concat(frames)
pit_sample_2025.to_csv('pit_sample_2025.csv')

varlist = ['gross_income', 'tax_payable', 'tot_emp_income', 
           'tax_on_rent_income', 'interest_dividend',
           'CGT_1_diff_being_adjusted_capital_gain',
           'CGT_1_diff_being_adjusted_capital_gain',
           'CGT_1_diff_being_adjusted_capital_gain',
           ]
total_weight_sample = pit_sample_2025['weight'].sum()
total_weight_population = pit_df_2025['weight'].sum()
#comparing the statistic of the population and sample
for var in varlist:
    pit_sample_2025['weighted_'+var] = pit_sample_2025[var]*pit_sample_2025['weight']
    sample_sum = pit_sample_2025['weighted_'+var].sum()
    population_sum = pit_df_2025[var].sum()
    print("            Sample Sum for ", var, " = ", sample_sum)
    print("        Population Sum for ", var, " = ", population_sum)
    print(" Sampling Error for Sum(%) ", var, " = ", "{:.2%}".format((population_sum-sample_sum)/population_sum))
    sample_mean = sample_sum/total_weight_sample
    population_mean = population_sum/total_weight_population
    print("           Sample Mean for ", var, " = ", sample_mean)
    print("       Population Mean for ", var, " = ", population_mean)
    print("Sampling Error for Mean(%) ", var, " = ", "{:.2%}".format((population_mean-sample_mean)/population_mean))    
