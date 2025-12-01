"""
This script is the generator of all cases. Turn on ***write=True*** option to save figures.
"""

from mfm import *
from read_file import *
from case1 import *
from case2 import *
from case3 import *
from case4 import *
from case5 import *

write_option = False
# write_option = True

case1 = case_1_error_compensation(write = write_option)
case1.plot_sensitivity()
case1.plot_error_compensation()

case2 = case_2_low_variability(write = write_option)
case2.low_variability()
case2.sensitivity()

case3 = case_3_phase_error(write = write_option)
case3.geometry()
case3.decoupling()
case3.sensitivity()

case4 = case_4_real_world_data(write = write_option)
case4.two_examples()
case4.radar()
case4.spatial_distribution()

case5 = case_5_sensitivity(write = write_option)
case5.sensitivity()