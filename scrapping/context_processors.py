from .models import LastDatabaseUpdateTime, SiteUpdateStatus, EventInfo


def last_database_update_time_processor(request):
    categories = LastDatabaseUpdateTime.objects.all()
    last_update = ''
    total_days = 0
    for i in categories:
        last_update = i.last_database_update_time
        total_days = i.days_database_active

    return {'last_update': last_update,
            'total_days': total_days,
            }



def site_update_status(request):
    status_obj = SiteUpdateStatus.objects.all()
    current_status = ''
    for i in status_obj:
        current_status = i.update_status

    return {'current_status': current_status,
            }



def last_daily_date(request):

    date_obj = EventInfo.objects.filter(event_category__exact='Daily')

    # If date_obj is empty return nothing. This will happen when database is empty.
    if not date_obj:
        return ''

    unclean_date_list = []
    for i in date_obj:
        unclean_date_list.append(i.date)

    split_datelist = []
    for i in unclean_date_list:
        split_datelist.append(i.split('.'))

    change_year_position_list = []
    for i in split_datelist:
        i[0], i[1], i[2] = i[2], i[0], i[1]
        change_year_position_list.append(i)

    change_year_position_list.sort()

    ordered_list_of_lists = []
    for i in change_year_position_list:
        i[2], i[0], i[1] = i[0], i[1], i[2]
        ordered_list_of_lists.append(i)

    ordered_date_list = []
    for i in ordered_list_of_lists:
        ordered_date_list.append('.'.join(i))


    return {'last_date': ordered_date_list[-1],
            }

