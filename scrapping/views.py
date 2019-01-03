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



















"""------------------------------------------------TOP DRIVERS VIEWS------------------------------------------------"""
# START for Top Drivers Sort Countries.
def top_drivers_sort_countries_view(request):
    object_ordered = PlayersInfo.objects.order_by('country_from', 'average_finish_place')

    drivers = pagination(request, object_ordered)


    context = {}

    context['drivers'] = drivers
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_drivers'] = total_qualified_drivers()

    return render(request, 'top_drivers/top_drivers_sort_countries.html', context)
# END for Top Drivers Sort Countries.


# START for Top Drivers Events Finished.
def top_drivers_events_finished_view(request):
    object_ordered = PlayersInfo.objects.order_by('-events_finished')

    drivers = pagination(request, object_ordered)


    context = {}

    context['drivers'] = drivers
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_drivers'] = total_qualified_drivers()

    return render(request, 'top_drivers/top_drivers_events_finished.html', context)
# END for Top Drivers Events Finished.


# START for Top Drivers Average Place.
def top_drivers_average_place_view(request):
    object_ordered = PlayersInfo.objects.order_by('average_finish_place')

    drivers = pagination(request, object_ordered)


    context = {}

    context['drivers'] = drivers
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_drivers'] = total_qualified_drivers()

    return render(request, 'top_drivers/top_drivers_average_place.html', context)
# END for Top Drivers Average Place.


# START for Top Drivers First Places.
def top_drivers_first_places_view(request):
    object_ordered = PlayersInfo.objects.order_by('-first_places', 'average_finish_place')

    drivers = pagination(request, object_ordered)


    context = {}

    context['drivers'] = drivers
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_drivers'] = total_qualified_drivers()

    return render(request, 'top_drivers/top_drivers_first_places.html', context)
# END for Top Drivers First Places.


# START for Top Drivers Top 3.
def top_drivers_top_3_view(request):
    object_ordered = PlayersInfo.objects.order_by('-top_3', 'average_finish_place')

    drivers = pagination(request, object_ordered)


    context = {}

    context['drivers'] = drivers
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_drivers'] = total_qualified_drivers()

    return render(request, 'top_drivers/top_drivers_top3.html', context)
# END for Top Drivers Top 3.


# START for Top Drivers Top 10.
def top_drivers_top_10_view(request):
    object_ordered = PlayersInfo.objects.order_by('-top_10', 'average_finish_place')

    drivers = pagination(request, object_ordered)


    context = {}

    context['drivers'] = drivers
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_drivers'] = total_qualified_drivers()

    return render(request, 'top_drivers/top_drivers_top10.html', context)
# END for Top Drivers Top 10.


# START for Top Drivers Top 100.
def top_drivers_top_100_view(request):
    object_ordered = PlayersInfo.objects.order_by('-top_100', 'average_finish_place')

    drivers = pagination(request, object_ordered)


    context = {}

    context['drivers'] = drivers
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_drivers'] = total_qualified_drivers()

    return render(request, 'top_drivers/top_drivers_top100.html', context)
# END for Top Drivers Top 100.


# START for Top Drivers Total Driving Time.
def top_drivers_driving_time_view(request):
    object_ordered = PlayersInfo.objects.order_by('-total_driving_time_seconds')

    drivers = pagination(request, object_ordered)


    context = {}

    context['drivers'] = drivers
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_drivers'] = total_qualified_drivers()

    return render(request, 'top_drivers/top_drivers_driving_time.html', context)
# END for Top Drivers Total Driving Time.
"""------------------------------------------------TOP DRIVERS VIEWS------------------------------------------------"""

















"""------------------------------------------------TOP COUNTRIES VIEWS------------------------------------------------"""
# START for Top Countries Sort Countries.
def top_countries_sort_countries_view(request):
    object_ordered = CountriesInfo.objects.order_by('country_name')


    context = {}

    context['object_ordered'] = object_ordered
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_countries'] = total_qualified_countries()

    return render(request, 'top_countries/top_countries_sort_countries.html', context)
# END for Top Countries Sort Countries.


# START for Top Countries Number Of Drivers.
def top_countries_number_of_drivers_view(request):
    object_ordered = CountriesInfo.objects.order_by('-number_of_drivers')


    context = {}

    context['object_ordered'] = object_ordered
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_countries'] = total_qualified_countries()

    return render(request, 'top_countries/top_countries_number_of_drivers.html', context)
# END for Top Countries Number Of Drivers.


# START for Top Countries Events Finished.
def top_countries_events_finished_view(request):
    object_ordered = CountriesInfo.objects.order_by('-events_finished')


    context = {}

    context['object_ordered'] = object_ordered
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_countries'] = total_qualified_countries()

    return render(request, 'top_countries/top_countries_events_finished.html', context)
# END for Top Countries Events Finished.


# START for Top Countries Average Finish Place.
def top_countries_average_place_view(request):
    object_ordered = CountriesInfo.objects.order_by('average_finish_place')


    context = {}

    context['object_ordered'] = object_ordered
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_countries'] = total_qualified_countries()

    return render(request, 'top_countries/top_countries_average_place.html', context)
# END for Top Countries Average Finish Place.


# START for Top Countries First Places.
def top_countries_first_places_view(request):
    object_ordered = CountriesInfo.objects.order_by('-first_places', 'average_finish_place')


    context = {}

    context['object_ordered'] = object_ordered
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_countries'] = total_qualified_countries()

    return render(request, 'top_countries/top_countries_first_places.html', context)
# END for Top Countries First Places.


# START for Top Countries Top 3.
def top_countries_top_3_view(request):
    object_ordered = CountriesInfo.objects.order_by('-top_3', 'average_finish_place')


    context = {}

    context['object_ordered'] = object_ordered
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_countries'] = total_qualified_countries()

    return render(request, 'top_countries/top_countries_top3.html', context)
# END for Top Countries Top 3.


# START for Top Countries Top 10.
def top_countries_top_10_view(request):
    object_ordered = CountriesInfo.objects.order_by('-top_10', 'average_finish_place')


    context = {}

    context['object_ordered'] = object_ordered
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_countries'] = total_qualified_countries()

    return render(request, 'top_countries/top_countries_top10.html', context)
# END for Top Countries Top 10.


# START for Top Countries Top 100.
def top_countries_top_100_view(request):
    object_ordered = CountriesInfo.objects.order_by('-top_100', 'average_finish_place')


    context = {}

    context['object_ordered'] = object_ordered
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_countries'] = total_qualified_countries()

    return render(request, 'top_countries/top_countries_top100.html', context)
# END for Top Countries Top 100.


# START for Top Countries Total Driving Time.
def top_countries_driving_time_view(request):
    object_ordered = CountriesInfo.objects.order_by('-total_driving_time_seconds')


    context = {}

    context['object_ordered'] = object_ordered
    context['total_unique_drivers'] = total_unique_drivers()
    context['total_qualified_countries'] = total_qualified_countries()


    return render(request, 'top_countries/top_countries_driving_time.html', context)
# END for Top Countries Total Driving Time.
"""------------------------------------------------TOP COUNTRIES VIEWS------------------------------------------------"""





























"""------------------------------------------------DRIVERS STATS VIEWS------------------------------------------------"""
# START for Drivers Stats.
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
# END for Drivers Stats.
"""------------------------------------------------DRIVERS STATS VIEWS------------------------------------------------"""






















"""------------------------------------------------ALL EVENTS VIEWS------------------------------------------------"""
# START for All Events.
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
# END for All Events.
"""------------------------------------------------ALL EVENTS VIEWS------------------------------------------------"""





















"""------------------------------------------------HOW THIS SITE WORKS VIEWS------------------------------------------------"""
# START for How This Site Works.
def how_this_site_works_view(request):

    context = {}


    return render(request, 'how_this_site_works.html', context)
# END for How This Site Works.
"""------------------------------------------------HOW THIS SITE WORKS VIEWS------------------------------------------------"""

















