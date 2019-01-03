from .models import LastDatabaseUpdateTime, SiteUpdateStatus

def last_database_update_time_processor(request):
    categories = LastDatabaseUpdateTime.objects.all()
    last_update = ''
    total_days = 0
    for i in categories:
        last_update = i.last_database_update_time
        total_days = i.days_database_active

    return {'last_update': last_update,
            'total_days': total_days
            }


def site_update_status(request):
    status_obj = SiteUpdateStatus.objects.all()
    current_status = ''
    for i in status_obj:
        current_status = i.update_status

    return {'current_status': current_status,
            }

