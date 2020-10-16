import math
import datetime
import os

from domain import *
from enviroment import *

base_folder = BASEDIR+DOMAIN + "/GRIB"
run_wps_folder = BASEDIR+DOMAIN +"/run_wps"

def metgrid():
    os.chdir(run_wps_folder)
    os.system(WPS_DIST+"metgrid.exe")



if __name__ == "__main__":
    metgrid()