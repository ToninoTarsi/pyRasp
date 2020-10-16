from typing import Dict, Any, Union, Optional
import math
import datetime
import os
import glob
import shutil
import string
import itertools
import yaml
import f90nml
from io import StringIO

from namelist import *

from domain import *
from enviroment import *

run_wrf_folder = BASEDIR+DOMAIN +"/run_wrf"

def wrf():

    os.chdir(run_wrf_folder)
    os.system(WRF_DIST+"wrf.exe")
    pass

if __name__ == "__main__":
    wrf()