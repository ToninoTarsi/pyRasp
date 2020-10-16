# pyRasp 
# Copyright (c) Tonino Tarsi 2020. Licensed under MIT.

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

SCHEMA_VAR_TYPES = {
    'str': str,
    'int': int,
    'real': float,
    'bool': bool,
    'list': list
}
SCHEMA_CACHE = {} # type: Dict[str,Any]
SCHEMA_DIR = os.path.join(os.path.dirname(__file__),  'nml_schemas')


def read_namelist(path: Union[str, StringIO], schema_name: Optional[str]=None) -> dict:
    if isinstance(path, str) and not os.path.exists(path):
        raise Exception(f'Namelist file {path} does not exist')
    try:
        nml = f90nml.read(path)
    except:
        # f90nml does not raise useful exceptions, so we can't include details here
        raise Exception(f'Namelist file {path} could not be parsed')
    
    # If a schema is specified, use it to fix single-element lists which are parsed as
    # primitive value since there is nothing to distinguish them from each other in the namelist format.
    if schema_name:
        schema = get_namelist_schema(schema_name)
        for group_name, group in nml.items():
            schema_group = schema[group_name]
            for var_name, var_val in group.items():
                schema_var = schema_group[var_name]
                schema_type = SCHEMA_VAR_TYPES[schema_var['type']]
                if schema_type is list and not isinstance(var_val, list):
                    group[var_name] = [var_val]
    return nml

def get_namelist_schema(name: str) -> dict:
    if name not in SCHEMA_CACHE:
        schema_path = os.path.join(SCHEMA_DIR, name + '.yml')
        with open(schema_path, encoding='utf-8') as f:
            schema = yaml.load(f,Loader=yaml.FullLoader)
        # Enforce lower-case keys to ease processing.
        # Note that Fortran is case-insensitive.
        schema = {
            group_name.lower(): {
                var_name.lower(): var_val
                for var_name, var_val in group.items()
            }
            for group_name, group in schema.items()
        }
        SCHEMA_CACHE[name] = schema
    return SCHEMA_CACHE[name]

def write_namelist(namelist: dict, path: str) -> None:
    nml = f90nml.Namelist(namelist)
    nml.indent = 0
    nml.write(path, force=True)