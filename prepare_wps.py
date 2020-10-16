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

def prepare_wps(download_result:dict):

    # Remove old files
    for path in glob.glob(os.path.join(run_wps_folder, 'GRIBFILE.*')):
        os.remove(path)
    for path in glob.glob(os.path.join(run_wps_folder, 'FILE_*')):
        os.remove(path)
    for path in glob.glob(os.path.join(run_wps_folder, 'met_em*')):
        os.remove(path)

    # Copy with WRF names 
    for path, ext in zip(download_result['paths'], generate_gribfile_extensions()):
        link_path = os.path.join(run_wps_folder, 'GRIBFILE.' + ext)
        shutil.copy(os.path.join(base_folder, path), link_path)
    
    namelist_wps =  os.path.join(run_wps_folder, "namelist.wps")
    nml = read_namelist(namelist_wps, schema_name='wps')

    max_dom = nml['share']['max_dom']
    for i in range(0,max_dom):
        nml['share']['start_date'][i] = download_result['time_range'][0].replace(" ","_")
        nml['share']['end_date'][i] = download_result['time_range'][1].replace(" ","_")

    write_namelist(nml,namelist_wps )
    print ('Prepare_wps completed')

    pass

def generate_gribfile_extensions():
    letters = list(string.ascii_uppercase)
    for a, b, c in itertools.product(letters, repeat=3):
        yield a + b + c





if __name__ == "__main__":
    result = {
        'dataset': 'null', 
        'product': 'null', 
        'time_range': ['2020-10-16 07:00:00', '2020-10-16 18:00:00'], 
        'interval_seconds': 3600, 
        'paths': ['gfs.t06z.pgrb2.0p25.f001', 'gfs.t06z.pgrb2.0p25.f002', 'gfs.t06z.pgrb2.0p25.f003', 'gfs.t06z.pgrb2.0p25.f004', 'gfs.t06z.pgrb2.0p25.f005', 'gfs.t06z.pgrb2.0p25.f006', 'gfs.t06z.pgrb2.0p25.f007', 'gfs.t06z.pgrb2.0p25.f008', 'gfs.t06z.pgrb2.0p25.f009', 'gfs.t06z.pgrb2.0p25.f010', 'gfs.t06z.pgrb2.0p25.f011', 'gfs.t06z.pgrb2.0p25.f012'], 
        'base_folder': 'E:/Rasp/gis4wrf/projects/CUCCOHD/GRIB', 
        'vtable': 'Vtable.GFS'
    }
    prepare_wps(result)