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
def cal_total_cit(ADJST_TAXABLE_INCOME_M_9, General_Rate, citax):
    """
    Compute Total CIT.
    """
    citax = General_Rate*ADJST_TAXABLE_INCOME_M_9
    citax = max(0, citax)
    return citax