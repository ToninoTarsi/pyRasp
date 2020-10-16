# pyRasp 
# Copyright (c) Tonino Tarsi 2020. Licensed under MIT.

import glob
import math
import datetime
import os
from typing import Iterable
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from domain import *

base_folder = BASEDIR+DOMAIN + "/GRIB" 


def downloadGFSA(overwrite=True) -> dict :

    if (overwrite):
        for path in glob.glob(os.path.join(base_folder, 'gfs.*')):
            os.remove(path)

    current_utc = datetime.datetime.utcnow().hour
    current_day = datetime.datetime.now().strftime("%Y%m%d")
    init_time = int(math.floor((current_utc -3 ) / 6 ) * 6)
    print("GFS Init Time: %2.2d" % init_time )
    start = DOMAIN1_STARTHH + DAY*24
    if (start % 24) < init_time :
        start = start + 24
    print("Start hour: %2.2d" % start )
    today = datetime.date.today()
    time_range = []
    forecast_date_start = datetime.datetime(today.year,today.month,today.day) + datetime.timedelta(hours=start)
    time_range.append(forecast_date_start.strftime("%Y-%m-%d %H:%M:00") )
    forecast_date_end = datetime.datetime(today.year,today.month,today.day) + datetime.timedelta(hours=start+(DOMAIN1_ENDHH-DOMAIN1_STARTHH))
    time_range.append(forecast_date_end.strftime("%Y-%m-%d %H:%M:00"))

    print("Forecast start: " + forecast_date_start.strftime("%Y-%m-%d %H:%M:00") )
    print("Forecast end  : " + forecast_date_end.strftime("%Y-%m-%d %H:%M:00")  )

    paths = []


    for i in range (0, DOMAIN1_ENDHH-DOMAIN1_STARTHH+1):
        forecast = (start + i - init_time)
        gfs_file =  "gfs.t%2.2dz.pgrb2.0p25.f%3.3d" % (init_time, forecast ) 
        paths.append(gfs_file)
        gfsb_file =  "gfs.t%2.2dz.pgrb2b.0p25.f%3.3d" % (init_time, forecast ) 
        gfs_area = "&subregion=&leftlon=%d&rightlon=%d&toplat=%d&bottomlat=%d" % (GRIB_LEFT_LON,GRIB_RIGHT_LON,GRIB_TOP_LAT,GRIB_BOTTOM_LAT)
        gfs_day = "&dir=/gfs.%s/%2.2d" % (current_day,init_time)
        grib_path = os.path.join(BASEDIR+DOMAIN+"/GRIB" ,gfs_file)

        use_old = (not overwrite) and  os.path.isfile(grib_path)

        # main data
        the_url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=" + gfs_file + "&all_lev=on&all_var=on" +  gfs_area +  gfs_day
        print("Downloading " + gfs_file + " ... ")
        if ( not use_old):
            download_file(the_url, grib_path )

        # secondary data
        the_url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25b.pl?file=" + gfsb_file + "&all_lev=on&all_var=on" +  gfs_area +  gfs_day
        grib_path_tmpb = grib_path + "b.tmp"
        print("Downloading " + gfsb_file + " ... ")
        if ( not use_old):
            download_file(the_url, grib_path_tmpb )

        # concatenate
        if ( not use_old):
            with open(grib_path, "ab") as myfile, open(grib_path_tmpb, "rb") as file2:
                myfile.write(file2.read())
            myfile.close()
            file2.close()
            os.remove(grib_path_tmpb) 




    result = {
        "dataset": "null",
        "product": "null",
        "time_range": time_range,
        "interval_seconds": 3600,
        'paths': paths,
        "base_folder": base_folder,
        "vtable": "Vtable.GFS"
    }

    return result


def download_file(url: str, path: str, session=None) -> None:
    for _ in download_file_with_progress(url, path, session):
        pass

def download_file_with_progress(url: str, path: str, session=None) -> Iterable[float]:
    new_session = session is None
    if new_session:
        session = requests_retry_session()
    try:
        response = session.get(url, stream=True)
        response.raise_for_status()
        total = response.headers.get('content-length')
        if total is not None:
            total = int(total)
        downloaded = 0
        with open(path, 'wb') as f:
            for data in response.iter_content(chunk_size=1024*1024):
                downloaded += len(data)
                f.write(data)
                if total is not None:
                    yield downloaded / total
        if total is None:
            yield 1.0
        else:
            assert total == downloaded, f'Did not receive all data: {total} != {downloaded}'
    finally:
        if new_session:
            session.close()

# https://www.peterbe.com/plog/best-practice-with-retries-with-requests
def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        status=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session



if __name__ == "__main__":
    print (downloadGFSA())


