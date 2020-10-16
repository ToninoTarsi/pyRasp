from typing import Dict, Any, Union, Optional
import math
import os
import glob
import shutil
import string
import itertools
import yaml
import f90nml
from io import StringIO
import datetime

from namelist import *

from domain import *
from enviroment import *

run_wrf_folder = BASEDIR+DOMAIN +"/run_wrf"
run_wps_folder = BASEDIR+DOMAIN +"/run_wps"

def prepare_wrf(download_result):

    for path in glob.glob(os.path.join(run_wrf_folder, 'met_em.*')):
        os.remove(path)
    for path in glob.glob(os.path.join(run_wps_folder, 'met_em.*')):
        os.rename(path,os.path.join(run_wrf_folder,os.path.basename(path)))

    forecast_date_start = datetime.datetime.strptime(download_result['time_range'][0],"%Y-%m-%d %H:%M:00") 
    forecast_date_end = datetime.datetime.strptime(download_result['time_range'][1],"%Y-%m-%d %H:%M:00") 

    start_year = forecast_date_start.year
    start_month = forecast_date_start.month
    start_day = forecast_date_start.day
    start_hour = forecast_date_start.hour
    start_minute = forecast_date_start.minute
    start_second = forecast_date_start.second
    end_year = forecast_date_end.year
    end_month = forecast_date_end.month
    end_day = forecast_date_end.day
    end_hour = forecast_date_end.hour
    end_minute = forecast_date_end.minute
    end_second = forecast_date_end.second
    
    namelist_input =  os.path.join(run_wrf_folder, "namelist.input")
    nml = read_namelist(namelist_input, schema_name='wrf')

    max_dom = nml['domains']['max_dom']
    for i in range(0,max_dom):
        nml['time_control']['start_year'][i] = start_year
        nml['time_control']['start_month'][i] = start_month
        nml['time_control']['start_day'][i] = start_day
        nml['time_control']['start_hour'][i] = start_hour
        nml['time_control']['start_minute'][i] = start_minute
        nml['time_control']['start_second'][i] = start_second
        nml['time_control']['end_year'][i] = end_year
        nml['time_control']['end_month'][i] = end_month
        nml['time_control']['end_day'][i] = end_day
        nml['time_control']['end_hour'][i] = end_hour
        nml['time_control']['end_minute'][i] = end_minute
        nml['time_control']['end_second'][i] = end_second

    #print(nml)
    write_namelist(nml,namelist_input )
    
    print ('prepare_wrf completed')

    pass





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
    prepare_wrf(result)