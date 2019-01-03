"""DirtRally URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url


from scrapping.views import driverstats_view, all_events_view, how_this_site_works_view


from scrapping.views import top_drivers_sort_countries_view, top_drivers_events_finished_view, top_drivers_average_place_view,\
top_drivers_first_places_view, top_drivers_top_3_view, top_drivers_top_10_view, top_drivers_top_100_view, top_drivers_driving_time_view


from scrapping.views import top_countries_sort_countries_view, top_countries_number_of_drivers_view, top_countries_events_finished_view,\
top_countries_average_place_view, top_countries_average_place_view, top_countries_first_places_view, top_countries_top_3_view,\
top_countries_top_10_view, top_countries_top_100_view, top_countries_driving_time_view



urlpatterns = [
    url('admin/', admin.site.urls),

    url('top_drivers_sort_countries/', top_drivers_sort_countries_view, name='top_drivers_sort_countries'),
    url('top_drivers_events_finished/', top_drivers_events_finished_view, name='top_drivers_events_finished'),
    url('top_drivers_average_place/', top_drivers_average_place_view, name='top_drivers_average_place'),
    url('top_drivers_first_places/', top_drivers_first_places_view, name='top_drivers_first_places'),
    url('top_drivers_top_3/', top_drivers_top_3_view, name='top_drivers_top_3'),
    url('top_drivers_top_10/', top_drivers_top_10_view, name='top_drivers_top_10'),
    url('top_drivers_top_100/', top_drivers_top_100_view, name='top_drivers_top_100'),
    url('top_drivers_driving_time/', top_drivers_driving_time_view, name='top_drivers_driving_time'),

    url('top_countries_sort_countries/', top_countries_sort_countries_view, name='top_countries_sort_countries'),
    url('top_countries_number_of_drivers/', top_countries_number_of_drivers_view, name='top_countries_number_of_drivers'),
    url('top_countries_events_finished/', top_countries_events_finished_view, name='top_countries_events_finished'),
    url('top_countries_average_place/', top_countries_average_place_view, name='top_countries_average_place'),
    url('top_countries_first_places/', top_countries_first_places_view, name='top_countries_first_places'),
    url('top_countries_top_3/', top_countries_top_3_view, name='top_countries_top_3'),
    url('top_countries_top_10/', top_countries_top_10_view, name='top_countries_top_10'),
    url('top_countries_top_100/', top_countries_top_100_view, name='top_countries_top_100'),
    url('top_countries_driving_time/', top_countries_driving_time_view, name='top_countries_driving_time'),

    path('driverstats/<drivers_id>/', driverstats_view, name='driverstats'),
    url('all_events/', all_events_view, name='all_events'),
    url('how_this_site_works/', how_this_site_works_view, name='how_this_site_works'),
    # path('my_stats', include('scrapping.urls'))
]
