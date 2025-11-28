"""
This script is the generator of all cases. Turn on ***write=True*** to save figures.
"""

from mfm import *
from read_file import *
from case1 import *
from case2 import *
from case3 import *
from case4 import *
from case5 import *

# case1 = case_1_error_compensation()
case1 = case_1_error_compensation(write=True)
case1.plot_sensitivity()
case1.plot_error_compensation()

# case2 = case_2_low_variability()
case2 = case_2_low_variability(write=True)
case2.low_variability()
case2.sensitivity()

# case3 = case_3_phase_error()
case3 = case_3_phase_error(write=True)
case3.geometry()
case3.decoupling()
case3.sensitivity()

# case4 = case_4_real_world_data()
case4 = case_4_real_world_data(write=True)
case4.two_examples()
case4.radar()
case4.spatial_distribution()

# case5 = case_5_sensitivity()
case5 = case_5_sensitivity(write=True)
case5.sensitivity()