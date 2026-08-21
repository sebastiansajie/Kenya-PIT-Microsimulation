"""
pitaxcalc-demo functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit

@iterate_jit(nopython=True)
def cal_capital_income(interest_dividend, capital_gains_1, capital_gains_2,
                       capital_gains_1P, tot_rent_income,
                           capital_income):
    """
    Compute total gross income.
    """
    capital_income = (interest_dividend+ capital_gains_1+capital_gains_2+
                           capital_gains_1P+tot_rent_income)
    return capital_income

@iterate_jit(nopython=True)
def cal_total_income(emp_income, capital_income, business_income,     
                           total_income):
    """
    Compute total gross income.
    """
    total_income = (emp_income+capital_income+business_income)
    return total_income

@iterate_jit(nopython=True)
def cal_emp_income(emp_income, emp_income_total):
    """
    Compute total gross income.
    """
    emp_income_total = (emp_income)
    return emp_income_total

@iterate_jit(nopython=True)
def cal_mortgage_deduction(mortgage_deduction_threshold, mortage_interest,     
                           mortgage_deduction):
    """
    Compute total gross income.
    """
    mortgage_deduction = min(mortgage_deduction_threshold, mortage_interest)
    return mortgage_deduction

@iterate_jit(nopython=True)
def cal_pension_deduction(pension_deduction_threshold, pension_contribution,     
                           pension_deduction):
    """
    Compute total gross income.
    """
    pension_deduction = min(pension_deduction_threshold, pension_contribution)
    return pension_deduction

@iterate_jit(nopython=True)
def cal_AHL_deduction(AHL_deduction_rate, emp_income,     
                           AHL_deduction):
    """
    Compute Affordable Housing Levy.
    """
    AHL_deduction = AHL_deduction_rate * emp_income
    return AHL_deduction

@iterate_jit(nopython=True)
def cal_SHIF_deduction(SHIF_deduction_rate, emp_income,     
                           SHIF_deduction):
    """
    Compute Affordable Housing Levy.
    """
    SHIF_deduction = SHIF_deduction_rate * emp_income
    return SHIF_deduction

@iterate_jit(nopython=True)
def cal_PRMF_deduction(PRMF_deduction_threshold, prmf_contribution,     
                           PRMF_deduction):
    """
    Compute Affordable Housing Levy.
    """
    PRMF_deduction = min(PRMF_deduction_threshold, prmf_contribution)
    return PRMF_deduction

@iterate_jit(nopython=True)
def cal_total_deductions(mortgage_deduction, pension_deduction, AHL_deduction,  
                           SHIF_deduction, PRMF_deduction, total_deductions):
    """
    Compute total gross income.
    """
    total_deductions = (mortgage_deduction+pension_deduction
                        +AHL_deduction + SHIF_deduction+PRMF_deduction)
    return total_deductions

@iterate_jit(nopython=True)
def cal_disability_exemption(disability_exemption_threshold, is_disabled,     
                           disability_exemption):
    """
    Compute total gross income.
    """
    if (is_disabled==1):
       disability_exemption = disability_exemption_threshold
    else:
       disability_exemption=0
    return disability_exemption

@iterate_jit(nopython=True)
def cal_net_taxable_income(tax_int_div_flat_rate, 
                           tax_cap_gains_flat_rate,
                           tax_rental_income_flat_rate,
                           disability_exemption, 
                           emp_income_total, business_income, 
                           interest_dividend, capital_gains_1,
                           capital_gains_1P, capital_gains_2,
                           tot_rent_income,
                           total_deductions,     
                           net_taxable_income):
    """
    Compute total gross income.
    """
    net_taxable_income = max(0, (emp_income_total+business_income
                          -total_deductions-disability_exemption))    
    
    if (tax_int_div_flat_rate==0):
        net_taxable_income = net_taxable_income + interest_dividend  
    if (tax_cap_gains_flat_rate==0):
        net_taxable_income = (net_taxable_income + max(0, capital_gains_1,
                              capital_gains_1P, capital_gains_2))  
    if (tax_rental_income_flat_rate==0):
        net_taxable_income = net_taxable_income + tot_rent_income
     
    net_taxable_income = max(0, net_taxable_income)    
    return net_taxable_income

@iterate_jit(nopython=True)
def cal_ti_behavior(rate1, rate2, rate3, rate4, rate5, rate6, rate7, 
                    tbrk1, tbrk2, tbrk3, tbrk4, tbrk5, tbrk6, tbrk7,
                    rate1_curr_law, rate2_curr_law, rate3_curr_law, 
                    rate4_curr_law, rate5_curr_law, rate6_curr_law, rate7_curr_law,
                    tbrk1_curr_law, tbrk2_curr_law, 
                    tbrk3_curr_law, tbrk4_curr_law, tbrk5_curr_law,
                    tbrk6_curr_law, tbrk7_curr_law,
                    elasticity_pit_taxable_income_threshold,
                    elasticity_pit_taxable_income_value, net_taxable_income,
                    income_wage_behavior):
    """
    Compute taxable total income after adjusting for behavior.
    """  
    elasticity_taxable_income_threshold0 = elasticity_pit_taxable_income_threshold[0]
    elasticity_taxable_income_threshold1 = elasticity_pit_taxable_income_threshold[1]
    #elasticity_taxable_income_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_taxable_income_value0=elasticity_pit_taxable_income_value[0]
    elasticity_taxable_income_value1=elasticity_pit_taxable_income_value[1]
    elasticity_taxable_income_value2=elasticity_pit_taxable_income_value[2]
    income_wage_l = net_taxable_income
    if income_wage_l<=0:
        elasticity=0
    elif income_wage_l<elasticity_taxable_income_threshold0:
        elasticity=elasticity_taxable_income_value0
    elif income_wage_l<elasticity_taxable_income_threshold1:
        elasticity=elasticity_taxable_income_value1
    else:
        elasticity=elasticity_taxable_income_value2

    if income_wage_l<0:
        marg_rate=0
    elif income_wage_l<=tbrk1:
        marg_rate=rate1
    elif income_wage_l<=tbrk2:
        marg_rate=rate2
    elif income_wage_l<=tbrk3:
        marg_rate=rate3        
    elif income_wage_l<=tbrk4:
        marg_rate=rate4
    elif income_wage_l<=tbrk5:
        marg_rate=rate5
    elif income_wage_l<=tbrk6:
            marg_rate=rate6
    else:         
        marg_rate=rate7
        
    if income_wage_l<0:
        marg_rate_curr_law=0
    elif income_wage_l<=tbrk1_curr_law:
        marg_rate_curr_law=rate1_curr_law
    elif income_wage_l<=tbrk2_curr_law:
        marg_rate_curr_law=rate2_curr_law
    elif income_wage_l<=tbrk3_curr_law:
        marg_rate_curr_law=rate3_curr_law
    elif income_wage_l<=tbrk4_curr_law:
        marg_rate_curr_law=rate4_curr_law    
    elif income_wage_l<=tbrk5_curr_law:
        marg_rate_curr_law=rate5_curr_law  
    elif income_wage_l<=tbrk6_curr_law:
        marg_rate_curr_law=rate6_curr_law          
    else:
        marg_rate_curr_law=rate7_curr_law
    
    frac_change_net_of_pit_rate = ((1-marg_rate)-(1-marg_rate_curr_law))/(1-marg_rate_curr_law)
    frac_change_income_wage = elasticity*(frac_change_net_of_pit_rate)  
    income_wage_behavior = income_wage_l*(1+frac_change_income_wage)
    return income_wage_behavior

@iterate_jit(nopython=True)
def cal_cap_gain_income_behavior(capital_gains_1_tax_rate, capital_gains_1P_tax_rate,
                    capital_gains_2_tax_rate, rental_income_tax_rate, 
                    interest_dividend_WHT_rate,
                    capital_gains_1_tax_rate_curr_law, capital_gains_1P_tax_rate_curr_law,
                    capital_gains_2_tax_rate_curr_law, rental_income_tax_rate_curr_law, 
                    interest_dividend_WHT_rate_curr_law,
                    elasticity_pit_capital_income_threshold,
                    elasticity_pit_capital_income_value, 
                    capital_gains_1, capital_gains_1P, 
                    capital_gains_2, interest_dividend, 
                    tot_rent_income,
                    capital_gains_1_behavior, capital_gains_1P_behavior, 
                    capital_gains_2_behavior, interest_dividend_behavior, 
                    tot_rent_income_behavior):
    """
    Compute taxable total income after adjusting for behavior.
    """
    elasticity_capital_income_threshold0 = elasticity_pit_capital_income_threshold[0]
    elasticity_capital_income_threshold1 = elasticity_pit_capital_income_threshold[1]
    #elasticity_taxable_income_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_capital_income_value0=elasticity_pit_capital_income_value[0]
    elasticity_capital_income_value1=elasticity_pit_capital_income_value[1]
    elasticity_capital_income_value2=elasticity_pit_capital_income_value[2]    
    
    def cal_income_behavior(income, tax_rate, tax_rate_curr_law):      
        if income<=0:
            elasticity=0
        elif income<elasticity_capital_income_threshold0:
            elasticity=elasticity_capital_income_value0
        elif income<elasticity_capital_income_threshold1:
            elasticity=elasticity_capital_income_value1
        else:
            elasticity=elasticity_capital_income_value2
        
        frac_change_net_of_tax_rate = ((1-tax_rate)-(1-tax_rate_curr_law))/(1-tax_rate_curr_law)
        frac_change_in_income = elasticity*(frac_change_net_of_tax_rate)  
        income_behavior = income*(1+frac_change_in_income)
        return income_behavior
    
    capital_gains_1_behavior = cal_income_behavior(capital_gains_1, capital_gains_1_tax_rate, capital_gains_1_tax_rate_curr_law)
    capital_gains_1P_behavior = cal_income_behavior(capital_gains_1P, capital_gains_1P_tax_rate, capital_gains_1P_tax_rate_curr_law)
    capital_gains_2_behavior = cal_income_behavior(capital_gains_2, capital_gains_2_tax_rate, capital_gains_2_tax_rate_curr_law)
    interest_dividend_behavior = cal_income_behavior(interest_dividend, interest_dividend_WHT_rate, interest_dividend_WHT_rate_curr_law)
    tot_rent_income_behavior = cal_income_behavior(tot_rent_income, rental_income_tax_rate, rental_income_tax_rate_curr_law)
    
    
    return capital_gains_1_behavior, capital_gains_1P_behavior, capital_gains_2_behavior, interest_dividend_behavior, tot_rent_income_behavior 

@iterate_jit(nopython=True)
def cal_cgt(tax_cap_gains_flat_rate, capital_gains_1_tax_rate,capital_gains_1P_tax_rate,
            capital_gains_2_tax_rate, capital_gains_1_behavior, capital_gains_1P_behavior,
            capital_gains_2_behavior, capital_gains_tax):
    """
    Compute Capital Gains Tax
    """
    if (tax_cap_gains_flat_rate==1):      
        capital_gains_tax = (capital_gains_1_tax_rate * capital_gains_1_behavior
                             + capital_gains_1P_tax_rate * capital_gains_1P_behavior
                             + capital_gains_2_tax_rate * capital_gains_2_behavior
                             )
    else:
        capital_gains_tax=0
    return capital_gains_tax

@iterate_jit(nopython=True)
def cal_rental_tax(tax_rental_income_flat_rate, rental_income_tax_rate, rental_income_exemption_threshold,
                   tot_rent_income, tot_rent_income_behavior, rental_income_tax):
    """
    Compute Affordable Housing Levy.
    """
    if (tax_rental_income_flat_rate==1):       
        if (tot_rent_income<=rental_income_exemption_threshold):
            rental_income_tax = 0 
        else:
            rental_income_tax = rental_income_tax_rate * tot_rent_income_behavior
    else:
        rental_income_tax=0
    return rental_income_tax

@iterate_jit(nopython=True)
def cal_WHT_interest_dividend(tax_int_div_flat_rate, interest_dividend_WHT_rate, interest_dividend_behavior, WHT_interest_dividend):
    """
    Compute PIT for Capital Income.
    """
    if (tax_int_div_flat_rate==1):
        WHT_interest_dividend = interest_dividend_WHT_rate*interest_dividend_behavior
    else:
        WHT_interest_dividend=0
    return WHT_interest_dividend

@iterate_jit(nopython=True)
def cal_pit_c(capital_gains_tax, rental_income_tax, WHT_interest_dividend, pitax_c):
    """
    Compute PIT for Capital Income.
    """
    pitax_c = capital_gains_tax+rental_income_tax+WHT_interest_dividend
    return pitax_c

@iterate_jit(nopython=True)
def cal_pit_w(rate1, rate2, rate3, rate4, rate5, rate6, rate7, 
              tbrk1, tbrk2, tbrk3, tbrk4, tbrk5, tbrk6, tbrk7,
              income_wage_behavior, pitax_w):
    """
    Compute PIT.
    """
    inc=income_wage_behavior
    pitax_w = (rate1 * min(inc, tbrk1) +
               rate2 * min(tbrk2 - tbrk1, max(0., inc - tbrk1)) +
               rate3 * min(tbrk3 - tbrk2, max(0., inc - tbrk2)) +
               rate4 * min(tbrk4 - tbrk3, max(0., inc - tbrk3)) +
               rate5 * min(tbrk5 - tbrk4, max(0., inc - tbrk4)) +
               rate6 * min(tbrk6 - tbrk5, max(0., inc - tbrk5)) +
               rate7 * max(0., inc - tbrk6))
    return pitax_w

@iterate_jit(nopython=True)
def cal_reliefs(personal_relief, insurance_relief_threshold, insurance_relief,     
                           total_reliefs):
    """
    Compute total gross income.
    """
    total_reliefs = personal_relief + min(insurance_relief_threshold, insurance_relief)
    return total_reliefs


@iterate_jit(nopython=True)
def cal_total_pit(pitax_w, pitax_c, total_reliefs, pitax):
    """
    Compute Total PIT.
    """
    pitax = max(0, pitax_w + pitax_c - total_reliefs)
    return pitax