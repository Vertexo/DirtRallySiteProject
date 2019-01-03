from django.contrib import admin

from .models import EventInfo, LeaderBoard, TotalUniqueDrivers, TotalQualifiedDrivers, NoCountryNameCheck, PlayersInfo,\
CountriesInfo, TotalQualifiedCountries, LastDatabaseUpdateTime, SiteUpdateStatus

# Register your models here.

admin.site.register(EventInfo)
admin.site.register(LeaderBoard)
admin.site.register(TotalUniqueDrivers)
admin.site.register(TotalQualifiedDrivers)
admin.site.register(NoCountryNameCheck)
admin.site.register(PlayersInfo)
admin.site.register(CountriesInfo)
admin.site.register(TotalQualifiedCountries)
admin.site.register(LastDatabaseUpdateTime)
admin.site.register(SiteUpdateStatus)
