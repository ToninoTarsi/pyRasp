# pyRasp 
# Copyright (c) Tonino Tarsi 2020. Licensed under MIT.

# requirement :
# Python 3 
# pip install pyyaml
# pip install request
# pip install f90nml


from downloadGFSA import downloadGFSA
from prepare_wps import prepare_wps
from ungrib import ungrib
from metgrid import metgrid
from prepare_wrf import prepare_wrf
from real import real
from wrf import wrf

result = downloadGFSA(True)
prepare_wps(result)
ungrib()
metgrid()
prepare_wrf(result)
real()
wrf()



