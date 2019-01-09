from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import EventInfo, LeaderBoard, TotalUniqueDrivers, TotalQualifiedDrivers, PlayersInfo,\
TotalQualifiedCountries, CountriesInfo





"""------------------------------------------------FUNCTIONS------------------------------------------------"""
# START of the code for getting integer value of total unique drivers on all leaderboard events.
def total_unique_drivers():
    total_unique_drivers_obj = TotalUniqueDrivers.objects.all()

    total_unique_drivers = 0
    for i in total_unique_drivers_obj:
        total_unique_drivers = i.player_id_list_len
    return total_unique_drivers
# END of the code for getting integer value of total unique drivers on all leaderboard events.


# START of the code for getting integer value of TotalQualifiedDrivers to templates.
def total_qualified_drivers():
    total_qualified_drivers_obj = TotalQualifiedDrivers.objects.all()

    total_qualified_drivers = 0
    for i in total_qualified_drivers_obj:
        total_qualified_drivers = i.qualified_drivers
    return total_qualified_drivers
# END of the code for getting integer value of TotalQualifiedDrivers to templates.


# START of the code for getting integer value of TotalQualifiedCountries to templates.
def total_qualified_countries():
    total_qualified_countries_obj = TotalQualifiedCountries.objects.all()

    total_qualified_countries = 0
    for i in total_qualified_countries_obj:
        total_qualified_countries = i.qualified_countries
    return total_qualified_countries
# END of the code for getting integer value of TotalQualifiedCountries to templates.


# START of the code for getting most participants ever and in what event.
def most_participants_ever():
    most_participants_ever_obj = EventInfo.objects.order_by('-total_drivers')

    most_participants_ever_list = []
    for i in most_participants_ever_obj:
        most_participants_ever_value = i.total_drivers
        most_participants_ever_event = i.event_category
        most_participants_ever_date = i.date
        most_participants_ever_list.append(most_participants_ever_value)
        most_participants_ever_list.append(most_participants_ever_event)
        most_participants_ever_list.append(most_participants_ever_date)

        return most_participants_ever_list
# END of the code for getting most participants ever and in what event.


# START pagination function.
def pagination(request, object):

    page = request.GET.get('page', 1)

    paginator = Paginator(object, 100)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return users
# END pagination function.
"""------------------------------------------------FUNCTIONS------------------------------------------------"""












"""------------------------------------------------TOP DRIVERS VIEW------------------------------------------------"""
def top_drivers_order_by_view(request, order_variable):

    th2_activity_tag = 'top_inactive_sort_button'
    th5_activity_tag = 'top_inactive_sort_button'
    th6_activity_tag = 'top_inactive_sort_button'
    th7_activity_tag = 'top_inactive_sort_button'
    th8_activity_tag = 'top_inactive_sort_button'
    th9_activity_tag = 'top_inactive_sort_button'
    th10_activity_tag = 'top_inactive_sort_button'
    th11_activity_tag = 'top_inactive_sort_button'


    object_ordered = PlayersInfo.objects.order_by(order_variable)

    if order_variable == 'country_from':
        object_ordered = PlayersInfo.objects.order_by(order_variable, 'average_finish_place')
        th2_activity_tag = 'top_active_sort_button'

    elif order_variable == 'events_finished':
        object_ordered = PlayersInfo.objects.order_by('-' + order_variable)
        th5_activity_tag = 'top_active_sort_button'

    elif order_variable == 'average_finish_place':
        object_ordered = PlayersInfo.objects.order_by(order_variable)
        th6_activity_tag = 'top_active_sort_button'

    elif order_variable == 'first_places' or order_variable == 'percentile_1st_place':
        object_ordered = PlayersInfo.objects.order_by('-' + order_variable, 'average_finish_place')
        th7_activity_tag = 'top_active_sort_button'

    elif order_variable == 'top_3' or order_variable == 'percentile_top_3':
        object_ordered = PlayersInfo.objects.order_by('-' + order_variable, 'average_finish_place')
        th8_activity_tag = 'top_active_sort_button'

    elif order_variable == 'top_10' or order_variable == 'percentile_top_10':
        object_ordered = PlayersInfo.objects.order_by('-' + order_variable, 'average_finish_place')
        th9_activity_tag = 'top_active_sort_button'

    elif order_variable == 'top_100' or order_variable == 'percentile_top_100':
        object_ordered = PlayersInfo.objects.order_by('-' + order_variable, 'average_finish_place')
        th10_activity_tag = 'top_active_sort_button'

    elif order_variable == 'total_driving_time_seconds':
        object_ordered = PlayersInfo.objects.order_by('-' + order_variable)
        th11_activity_tag = 'top_active_sort_button'


    drivers = pagination(request, object_ordered)

    context = {}

    context['drivers'] = drivers
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_drivers'] = total_qualified_drivers()
    context['th2_activity_tag'] = th2_activity_tag
    context['th5_activity_tag'] = th5_activity_tag
    context['th6_activity_tag'] = th6_activity_tag
    context['th7_activity_tag'] = th7_activity_tag
    context['th8_activity_tag'] = th8_activity_tag
    context['th9_activity_tag'] = th9_activity_tag
    context['th10_activity_tag'] = th10_activity_tag
    context['th11_activity_tag'] = th11_activity_tag

    return render(request, 'top_drivers.html', context)
"""------------------------------------------------TOP DRIVERS VIEW------------------------------------------------"""













"""------------------------------------------------TOP COUNTRIES VIEW------------------------------------------------"""
def top_countries_order_by_view(request, order_variable):

    th3_activity_tag = 'top_inactive_sort_button'
    th4_activity_tag = 'top_inactive_sort_button'
    th5_activity_tag = 'top_inactive_sort_button'
    th6_activity_tag = 'top_inactive_sort_button'
    th7_activity_tag = 'top_inactive_sort_button'
    th8_activity_tag = 'top_inactive_sort_button'
    th9_activity_tag = 'top_inactive_sort_button'
    th10_activity_tag = 'top_inactive_sort_button'
    th11_activity_tag = 'top_inactive_sort_button'

    object_ordered = CountriesInfo.objects.order_by(order_variable)

    if order_variable == 'country_name':
        object_ordered = CountriesInfo.objects.order_by(order_variable)
        th3_activity_tag = 'top_active_sort_button'

    elif order_variable == 'number_of_drivers':
        object_ordered = CountriesInfo.objects.order_by('-' + order_variable)
        th4_activity_tag = 'top_active_sort_button'

    elif order_variable == 'events_finished':
        object_ordered = CountriesInfo.objects.order_by('-' + order_variable)
        th5_activity_tag = 'top_active_sort_button'

    elif order_variable == 'average_finish_place':
        object_ordered = CountriesInfo.objects.order_by(order_variable)
        th6_activity_tag = 'top_active_sort_button'

    elif order_variable == 'first_places' or order_variable == 'percentile_1st_place':
        object_ordered = CountriesInfo.objects.order_by('-' + order_variable, 'average_finish_place')
        th7_activity_tag = 'top_active_sort_button'

    elif order_variable == 'top_3' or order_variable == 'percentile_top_3':
        object_ordered = CountriesInfo.objects.order_by('-' + order_variable, 'average_finish_place')
        th8_activity_tag = 'top_active_sort_button'

    elif order_variable == 'top_10' or order_variable == 'percentile_top_10':
        object_ordered = CountriesInfo.objects.order_by('-' + order_variable, 'average_finish_place')
        th9_activity_tag = 'top_active_sort_button'

    elif order_variable == 'top_100' or order_variable == 'percentile_top_100':
        object_ordered = CountriesInfo.objects.order_by('-' + order_variable, 'average_finish_place')
        th10_activity_tag = 'top_active_sort_button'

    elif order_variable == 'total_driving_time_seconds':
        object_ordered = CountriesInfo.objects.order_by('-' + order_variable)
        th11_activity_tag = 'top_active_sort_button'


    context = {}

    context['object_ordered'] = object_ordered
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_countries'] = total_qualified_countries()
    context['th3_activity_tag'] = th3_activity_tag
    context['th4_activity_tag'] = th4_activity_tag
    context['th5_activity_tag'] = th5_activity_tag
    context['th6_activity_tag'] = th6_activity_tag
    context['th7_activity_tag'] = th7_activity_tag
    context['th8_activity_tag'] = th8_activity_tag
    context['th9_activity_tag'] = th9_activity_tag
    context['th10_activity_tag'] = th10_activity_tag
    context['th11_activity_tag'] = th11_activity_tag

    return render(request, 'top_countries.html', context)
"""------------------------------------------------TOP COUNTRIES VIEW------------------------------------------------"""











"""------------------------------------------------DRIVERS STATS VIEW------------------------------------------------"""
def driverstats_view(request, drivers_id):

    object_ordered = PlayersInfo.objects.filter(player_id__exact=drivers_id)

    drivers_name = ''
    drivers_id = ''
    for i in object_ordered:
        drivers_name = i.name
        drivers_id = i.player_id

    context = {}

    context['drivers_name'] = drivers_name
    context['drivers_id'] = drivers_id

    return render(request, 'driver_stats.html', context)
"""------------------------------------------------DRIVERS STATS VIEW------------------------------------------------"""










"""------------------------------------------------ALL EVENTS VIEW------------------------------------------------"""
def all_events_view(request):

    obj = LeaderBoard.objects.filter(event_info__event_category__exact='Daily', event_info__date__exact='10.19.2018')

    position_list = []
    country_name_list = []
    name_list = []
    vehicle_list = []
    time_list = []
    time_seconds_list = []
    diff_1st_list = []
    player_id_list = []

    for i in obj:

        position_list.append(i.position)
        country_name_list.append(i.country_name)
        name_list.append(i.name)
        vehicle_list.append(i.vehicle)
        time_list.append(i.time)
        time_seconds_list.append(i.time_seconds)
        diff_1st_list.append(i.diff_1st)
        player_id_list.append(i.player_id)


    # START of reverse list script.
    reverse_list = position_list[::-1]
    position_list = reverse_list

    reverse_list = country_name_list[::-1]
    country_name_list = reverse_list

    reverse_list = name_list[::-1]
    name_list = reverse_list

    reverse_list = vehicle_list[::-1]
    vehicle_list = reverse_list

    reverse_list = time_list[::-1]
    time_list = reverse_list

    reverse_list = diff_1st_list[::-1]
    diff_1st_list = reverse_list

    reverse_list = player_id_list[::-1]
    player_id_list = reverse_list
    # END of reverse list script.


    zipped_leader_list = list(zip(position_list, country_name_list, name_list,
                                  player_id_list, vehicle_list,time_list, diff_1st_list
                                  ))

    date = ''
    event_name = ''
    location = ''
    stage = ''
    time_of_the_day = ''
    weather = ''
    total_drivers = 0

    for info in obj:

        date = info.event_info.date
        event_name = info.event_info.event_name
        location = info.event_info.location
        stage = info.event_info.stage
        time_of_the_day = info.event_info.time_of_the_day
        weather = info.event_info.weather
        total_drivers = info.event_info.total_drivers
        break


    context = {}

    context['date'] = date
    context['event_name'] = event_name
    context['location'] = location
    context['stage'] = stage
    context['time_of_the_day'] = time_of_the_day
    context['weather'] = weather
    context['total_drivers'] = total_drivers
    context['zipped_leader_list'] = zipped_leader_list
    context['total_unique_drivers'] = total_unique_drivers()
    context['most_participants_ever_value'] = most_participants_ever()[0]
    context['most_participants_ever_event'] = most_participants_ever()[1]
    context['most_participants_ever_date'] = most_participants_ever()[2]

    return render(request, 'all_events.html', context)
"""------------------------------------------------ALL EVENTS VIEW------------------------------------------------"""









"""------------------------------------------------HOW THIS SITE WORKS VIEW------------------------------------------------"""
def how_this_site_works_view(request):

    context = {}

    return render(request, 'how_this_site_works.html', context)
"""------------------------------------------------HOW THIS SITE WORKS VIEW------------------------------------------------"""






