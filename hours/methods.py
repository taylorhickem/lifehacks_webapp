from nthours import nowthen as nt
import datetime as dt
from hours.models import HrsAppParameter, HrsAppResource, ResourceStatus
from django.utils import timezone


def update_events():
    '''Update events database sqlite and gsheet with new NowThen records
    '''
    nt.load()
    nt.update_events()


def refresh_last_update():
    '''refresh the parameter 'last_updated' to the current time
    '''
    lu = HrsAppParameter.objects.filter(name='last_updated')[0]
    lu.datetime_value = timezone.now()
    lu.save()


def refresh_resources():
    refresh_db()
    refresh_gsheet()
    refresh_gdrive()
    refresh_last_update()


def refresh_db():
    status_str = 'ERROR'
    recent_date = None
    resource_name = 'mysql_db'
    yesterday_date = timezone.now().date() - dt.timedelta(days=1)

    # try to connect to resource
    # if cannnot connect, status is in error (default)
    # get recent_date = max date from field 'date' in table 'event'
    # if recent_date >= yesterday, sheet is current

    try:
        # 01 connect to resource
        nt.load()

        # 02 get most recent date
        db_events = nt.db.get_table('event')
        recent_date = db_events['date'].max().date()

        # 03 determine status
        if recent_date >= yesterday_date:
            status_str = 'CURRENT'
        else:
            status_str = 'PENDING UPDATE'

    except:
        print('failed to connect to %s' % resource_name)

    # 04 update the resource fields: status, recent_date
    update_resource(resource_name, status_str, recent_date)


def refresh_gsheet():
    status_str = 'ERROR'
    recent_date = None
    resource_name = 'gsheet_report'
    yesterday_date = timezone.now().date() - dt.timedelta(days=1)

    # try to connect to resource
    # if cannnot connect, status is in error (default)
    # get recent_date = max date from field 'date' in tab 'events'
    # if recent_date >= yesterday, sheet is current

    try:
        # 01 connect to resource
        nt.load()

        # 02 get most recent date
        gs_events = nt.db.get_sheet('events')
        recent_date = gs_events['date'].max().date()

        # 03 determine status
        if recent_date >= yesterday_date:
            status_str = 'CURRENT'
        else:
            status_str = 'PENDING UPDATE'

    except:
        print('failed to connect to %s' % resource_name)

    # 04 update the resource fields: status, recent_date
    update_resource(resource_name, status_str, recent_date)


def refresh_gdrive():
    status_str = 'ERROR'
    recent_date = None
    resource_name = 'gdrive_folder'

    def recent_date_from_records(records):
        rcd_dates = [nt.record_date_from_filename(rcd['filename']) for rcd in records]
        return max(rcd_dates)

    # try to connect to resource
    # if cannnot connect, status is in error (default)
    # if empty list, current
    # if not empty list, most recent date is.. most recent date

    try:
        nt.load()
        nt.new_records_asbytes = [] #force the list to empty

        nt.gdrive_load_csv()
        records = nt.new_records_asbytes

        if len(records) > 0:
            status_str = 'PENDING UPDATE'

            # 02 get most recent date
            recent_date = recent_date_from_records(records)
        else:
            status_str = 'CURRENT'

    except:
        print('failed to connect to %s' % resource_name)

    #04 update the resource fields: status, recent_date
    update_resource(resource_name, status_str, recent_date)


def update_resource(resource_name, status_str, recent_date):
    status = ResourceStatus.objects.filter(status=status_str)[0]
    resource = HrsAppResource.objects.filter(name=resource_name)[0]
    resource.status = status
    resource.recent_date = recent_date
    resource.save()