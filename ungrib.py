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

base_folder = BASEDIR+DOMAIN + "/GRIB"
run_wps_folder = BASEDIR+DOMAIN +"/run_wps"

def ungrib():

    os.chdir(run_wps_folder)
    os.system(WPS_DIST+"ungrib.exe")
    pass



if __name__ == "__main__":
    ungrib()