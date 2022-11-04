import json
import pandas as pd
from nthours import nowthen as nt


GSHEET_CONFIG_FILENAME = 'gsheet_categories_config.json'
TABLENAMES = [
    'roles',
    'projects',
    'activities'
]


def nt_load():
    nt.db.load_config()
    #overwrite gsheet config file location
    nt.db.GSHEET_CONFIG = json.load(open(GSHEET_CONFIG_FILENAME))
    nt.db.load_gsheet()


def nt_unload():
    nt.db.gs_engine = None


def get_table(table_name):
    tbl = None
    if table_name in TABLENAMES:
        if table_name == 'roles':
            tbl = get_roles_table()

        elif table_name == 'projects':
            tbl = get_projects_table()

        elif table_name == 'activities':
            tbl = get_activities_table()
    else:
        raise ValueError('the table: %s, does not exist' % table_name)

    return tbl


def get_roles_table():
    tbl = nt.db.get_sheet('roles').reset_index()
    tbl.rename(columns={'index': 'order', 'role': 'name'}, inplace=True)
    tbl['is_active'] = tbl['status'].apply(lambda x: x == 'active')
    del tbl['status']
    return tbl


def get_projects_table():
    tbl = None
    return tbl


def get_activities_table():
    tbl = None
    return tbl
