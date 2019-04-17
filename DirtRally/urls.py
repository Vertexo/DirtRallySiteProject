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

from scrapping.views import all_events_view, how_this_site_works_view, \
    top_drivers_order_by_view, top_countries_order_by_view, driverstats_view, countrystats_view

urlpatterns = [
    url('admin/', admin.site.urls),

    path('drivers_order_by/<event_category>/<order_variable>/', top_drivers_order_by_view, name='top_drivers_order_by_view'),
    path('countries_order_by/<event_category>/<order_variable>/', top_countries_order_by_view, name='top_countries_order_by_view'),
    path('driverstats/<drivers_id>/', driverstats_view, name='driverstats'),
    path('countrystats/<country_name>/<event_category>/<order_variable>/', countrystats_view, name='countrystats'),
    path('all_events/<event_category>/<date>/', all_events_view, name='all_events'),
    url('how_this_site_works/', how_this_site_works_view, name='how_this_site_works'),
    # url('how_this_site_works/', mypage, name='mypage'),
]
