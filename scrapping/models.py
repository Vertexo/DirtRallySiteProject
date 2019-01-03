from django.db import models


class EventInfo(models.Model):
    event_category = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    event_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    stage = models.CharField(max_length=50)
    time_of_the_day = models.CharField(max_length=50)
    weather = models.CharField(max_length=50)
    total_drivers = models.IntegerField()

    def __str__(self):
        return '{}_{}'.format(self.event_category, self.date)

    class Meta:
        ordering = ['event_category', 'date']


class LeaderBoard(models.Model):
    event_info = models.ForeignKey(EventInfo, on_delete=models.CASCADE)
    position = models.IntegerField()
    country_name = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    vehicle = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    time_seconds = models.FloatField()
    diff_1st = models.CharField(max_length=50)
    player_id = models.IntegerField()

    def __str__(self):
        return '{}_{}'.format(self.event_info, self.position)

    class Meta:
        ordering = ['-position']


# Database table for all unique players info.
class PlayersInfo(models.Model):
    country_from = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    player_id = models.IntegerField()
    events_finished = models.IntegerField()
    average_finish_place = models.FloatField()
    first_places = models.IntegerField()
    top_3 = models.IntegerField()
    top_10 = models.IntegerField()
    top_100 = models.IntegerField()
    percentile_1st_place = models.FloatField()
    percentile_top_3 = models.FloatField()
    percentile_top_10 = models.FloatField()
    percentile_top_100 = models.FloatField()
    total_driving_time_seconds = models.FloatField()
    total_driving_time_string = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.player_id)
    class Meta:
        ordering = ['player_id']


# Database table for all unique players info.
class CountriesInfo(models.Model):
    country_name = models.CharField(max_length=50)
    number_of_drivers = models.IntegerField()
    events_finished = models.IntegerField()
    average_finish_place = models.FloatField()
    first_places = models.IntegerField()
    top_3 = models.IntegerField()
    top_10 = models.IntegerField()
    top_100 = models.IntegerField()
    percentile_1st_place = models.FloatField()
    percentile_top_3 = models.FloatField()
    percentile_top_10 = models.FloatField()
    percentile_top_100 = models.FloatField()
    total_driving_time_seconds = models.FloatField()
    total_driving_time_string = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.country_name)

    class Meta:
        ordering = ['country_name']


# Database entry for integer on total unique players recorder on leaderboards.
class TotalUniqueDrivers(models.Model):
    player_id_list_len = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.player_id_list_len)


# Database entry for integer on total qualified countries for top tables.
class TotalQualifiedCountries(models.Model):
    qualified_countries = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.qualified_countries)


# Database entry for integer on total qualified drivers for top tables.
class TotalQualifiedDrivers(models.Model):
    qualified_drivers = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.qualified_drivers)


# Database table for counting if all uploaded drivers has registered country name.
class NoCountryNameCheck(models.Model):
    no_country_name = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.no_country_name)


# Database table for last database update in UTC time.
class LastDatabaseUpdateTime(models.Model):
    last_database_update_time = models.CharField(max_length=100)
    days_database_active = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.last_database_update_time)


# Database entry for database_operations status during the site's update phase.
class SiteUpdateStatus(models.Model):
    update_status = models.CharField(max_length=500)

    def __str__(self):
        return '{}'.format(self.update_status)
