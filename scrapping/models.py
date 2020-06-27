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
    earned_points = models.IntegerField()

    def __str__(self):
        return '{}_{}'.format(self.event_info, self.position)

    class Meta:
        ordering = ['-position']


# Database table for all unique players info.
class PlayersInfo(models.Model):
    country_from = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    player_id = models.IntegerField(blank=True, null=True)

    overall_events_finished = models.IntegerField(null=True, blank=True)
    overall_average_finish_place = models.FloatField(null=True, blank=True)
    overall_first_places = models.IntegerField(null=True, blank=True)
    overall_top_3 = models.IntegerField(null=True, blank=True)
    overall_top_10 = models.IntegerField(null=True, blank=True)
    overall_top_100 = models.IntegerField(null=True, blank=True)
    overall_driving_time_seconds = models.FloatField(null=True, blank=True)
    overall_points = models.IntegerField(null=True, blank=True)
    overall_average_points = models.IntegerField(null=True, blank=True)

    daily_events_finished = models.IntegerField(null=True, blank=True)
    daily_average_finish_place = models.FloatField(null=True, blank=True)
    daily_first_places = models.IntegerField(null=True, blank=True)
    daily_top_3 = models.IntegerField(null=True, blank=True)
    daily_top_10 = models.IntegerField(null=True, blank=True)
    daily_top_100 = models.IntegerField(null=True, blank=True)
    daily_driving_time_seconds = models.FloatField(null=True, blank=True)
    daily_points = models.IntegerField(null=True, blank=True)
    daily_average_points = models.IntegerField(null=True, blank=True)

    daily2_events_finished = models.IntegerField(null=True, blank=True)
    daily2_average_finish_place = models.FloatField(null=True, blank=True)
    daily2_first_places = models.IntegerField(null=True, blank=True)
    daily2_top_3 = models.IntegerField(null=True, blank=True)
    daily2_top_10 = models.IntegerField(null=True, blank=True)
    daily2_top_100 = models.IntegerField(null=True, blank=True)
    daily2_driving_time_seconds = models.FloatField(null=True, blank=True)
    daily2_points = models.IntegerField(null=True, blank=True)
    daily2_average_points = models.IntegerField(null=True, blank=True)

    weekly_events_finished = models.IntegerField(null=True, blank=True)
    weekly_average_finish_place = models.FloatField(null=True, blank=True)
    weekly_first_places = models.IntegerField(null=True, blank=True)
    weekly_top_3 = models.IntegerField(null=True, blank=True)
    weekly_top_10 = models.IntegerField(null=True, blank=True)
    weekly_top_100 = models.IntegerField(null=True, blank=True)
    weekly_driving_time_seconds = models.FloatField(null=True, blank=True)
    weekly_points = models.IntegerField(null=True, blank=True)
    weekly_average_points = models.IntegerField(null=True, blank=True)

    weekly2_events_finished = models.IntegerField(null=True, blank=True)
    weekly2_average_finish_place = models.FloatField(null=True, blank=True)
    weekly2_first_places = models.IntegerField(null=True, blank=True)
    weekly2_top_3 = models.IntegerField(null=True, blank=True)
    weekly2_top_10 = models.IntegerField(null=True, blank=True)
    weekly2_top_100 = models.IntegerField(null=True, blank=True)
    weekly2_driving_time_seconds = models.FloatField(null=True, blank=True)
    weekly2_points = models.IntegerField(null=True, blank=True)
    weekly2_average_points = models.IntegerField(null=True, blank=True)

    monthly_events_finished = models.IntegerField(null=True, blank=True)
    monthly_average_finish_place = models.FloatField(null=True, blank=True)
    monthly_first_places = models.IntegerField(null=True, blank=True)
    monthly_top_3 = models.IntegerField(null=True, blank=True)
    monthly_top_10 = models.IntegerField(null=True, blank=True)
    monthly_top_100 = models.IntegerField(null=True, blank=True)
    monthly_driving_time_seconds = models.FloatField(null=True, blank=True)
    monthly_points = models.IntegerField(null=True, blank=True)
    monthly_average_points = models.IntegerField(null=True, blank=True)


    overall_world_rank_events_finished = models.IntegerField(null=True, blank=True)
    overall_world_rank_points = models.IntegerField(null=True, blank=True)
    overall_world_rank_average_points = models.IntegerField(null=True, blank=True)
    overall_world_rank_average_finish_place = models.IntegerField(null=True, blank=True)
    overall_world_rank_first_places = models.IntegerField(null=True, blank=True)
    overall_world_rank_top_3 = models.IntegerField(null=True, blank=True)
    overall_world_rank_top_10 = models.IntegerField(null=True, blank=True)
    overall_world_rank_top_100 = models.IntegerField(null=True, blank=True)
    overall_world_rank_driving_time_seconds = models.IntegerField(null=True, blank=True)

    daily_world_rank_events_finished = models.IntegerField(null=True, blank=True)
    daily_world_rank_points = models.IntegerField(null=True, blank=True)
    daily_world_rank_average_points = models.IntegerField(null=True, blank=True)
    daily_world_rank_average_finish_place = models.IntegerField(null=True, blank=True)
    daily_world_rank_first_places = models.IntegerField(null=True, blank=True)
    daily_world_rank_top_3 = models.IntegerField(null=True, blank=True)
    daily_world_rank_top_10 = models.IntegerField(null=True, blank=True)
    daily_world_rank_top_100 = models.IntegerField(null=True, blank=True)
    daily_world_rank_driving_time_seconds = models.IntegerField(null=True, blank=True)

    daily2_world_rank_events_finished = models.IntegerField(null=True, blank=True)
    daily2_world_rank_points = models.IntegerField(null=True, blank=True)
    daily2_world_rank_average_points = models.IntegerField(null=True, blank=True)
    daily2_world_rank_average_finish_place = models.IntegerField(null=True, blank=True)
    daily2_world_rank_first_places = models.IntegerField(null=True, blank=True)
    daily2_world_rank_top_3 = models.IntegerField(null=True, blank=True)
    daily2_world_rank_top_10 = models.IntegerField(null=True, blank=True)
    daily2_world_rank_top_100 = models.IntegerField(null=True, blank=True)
    daily2_world_rank_driving_time_seconds = models.IntegerField(null=True, blank=True)

    weekly_world_rank_events_finished = models.IntegerField(null=True, blank=True)
    weekly_world_rank_points = models.IntegerField(null=True, blank=True)
    weekly_world_rank_average_points = models.IntegerField(null=True, blank=True)
    weekly_world_rank_average_finish_place = models.IntegerField(null=True, blank=True)
    weekly_world_rank_first_places = models.IntegerField(null=True, blank=True)
    weekly_world_rank_top_3 = models.IntegerField(null=True, blank=True)
    weekly_world_rank_top_10 = models.IntegerField(null=True, blank=True)
    weekly_world_rank_top_100 = models.IntegerField(null=True, blank=True)
    weekly_world_rank_driving_time_seconds = models.IntegerField(null=True, blank=True)

    weekly2_world_rank_events_finished = models.IntegerField(null=True, blank=True)
    weekly2_world_rank_points = models.IntegerField(null=True, blank=True)
    weekly2_world_rank_average_points = models.IntegerField(null=True, blank=True)
    weekly2_world_rank_average_finish_place = models.IntegerField(null=True, blank=True)
    weekly2_world_rank_first_places = models.IntegerField(null=True, blank=True)
    weekly2_world_rank_top_3 = models.IntegerField(null=True, blank=True)
    weekly2_world_rank_top_10 = models.IntegerField(null=True, blank=True)
    weekly2_world_rank_top_100 = models.IntegerField(null=True, blank=True)
    weekly2_world_rank_driving_time_seconds = models.IntegerField(null=True, blank=True)

    monthly_world_rank_events_finished = models.IntegerField(null=True, blank=True)
    monthly_world_rank_points = models.IntegerField(null=True, blank=True)
    monthly_world_rank_average_points = models.IntegerField(null=True, blank=True)
    monthly_world_rank_average_finish_place = models.IntegerField(null=True, blank=True)
    monthly_world_rank_first_places = models.IntegerField(null=True, blank=True)
    monthly_world_rank_top_3 = models.IntegerField(null=True, blank=True)
    monthly_world_rank_top_10 = models.IntegerField(null=True, blank=True)
    monthly_world_rank_top_100 = models.IntegerField(null=True, blank=True)
    monthly_world_rank_driving_time_seconds = models.IntegerField(null=True, blank=True)


    overall_country_rank_events_finished = models.IntegerField(null=True, blank=True)
    overall_country_rank_points = models.IntegerField(null=True, blank=True)
    overall_country_rank_average_points = models.IntegerField(null=True, blank=True)
    overall_country_rank_average_finish_place = models.IntegerField(null=True, blank=True)
    overall_country_rank_first_places = models.IntegerField(null=True, blank=True)
    overall_country_rank_top_3 = models.IntegerField(null=True, blank=True)
    overall_country_rank_top_10 = models.IntegerField(null=True, blank=True)
    overall_country_rank_top_100 = models.IntegerField(null=True, blank=True)
    overall_country_rank_driving_time_seconds = models.IntegerField(null=True, blank=True)

    daily_country_rank_events_finished = models.IntegerField(null=True, blank=True)
    daily_country_rank_points = models.IntegerField(null=True, blank=True)
    daily_country_rank_average_points = models.IntegerField(null=True, blank=True)
    daily_country_rank_average_finish_place = models.IntegerField(null=True, blank=True)
    daily_country_rank_first_places = models.IntegerField(null=True, blank=True)
    daily_country_rank_top_3 = models.IntegerField(null=True, blank=True)
    daily_country_rank_top_10 = models.IntegerField(null=True, blank=True)
    daily_country_rank_top_100 = models.IntegerField(null=True, blank=True)
    daily_country_rank_driving_time_seconds = models.IntegerField(null=True, blank=True)

    daily2_country_rank_events_finished = models.IntegerField(null=True, blank=True)
    daily2_country_rank_points = models.IntegerField(null=True, blank=True)
    daily2_country_rank_average_points = models.IntegerField(null=True, blank=True)
    daily2_country_rank_average_finish_place = models.IntegerField(null=True, blank=True)
    daily2_country_rank_first_places = models.IntegerField(null=True, blank=True)
    daily2_country_rank_top_3 = models.IntegerField(null=True, blank=True)
    daily2_country_rank_top_10 = models.IntegerField(null=True, blank=True)
    daily2_country_rank_top_100 = models.IntegerField(null=True, blank=True)
    daily2_country_rank_driving_time_seconds = models.IntegerField(null=True, blank=True)

    weekly_country_rank_events_finished = models.IntegerField(null=True, blank=True)
    weekly_country_rank_points = models.IntegerField(null=True, blank=True)
    weekly_country_rank_average_points = models.IntegerField(null=True, blank=True)
    weekly_country_rank_average_finish_place = models.IntegerField(null=True, blank=True)
    weekly_country_rank_first_places = models.IntegerField(null=True, blank=True)
    weekly_country_rank_top_3 = models.IntegerField(null=True, blank=True)
    weekly_country_rank_top_10 = models.IntegerField(null=True, blank=True)
    weekly_country_rank_top_100 = models.IntegerField(null=True, blank=True)
    weekly_country_rank_driving_time_seconds = models.IntegerField(null=True, blank=True)

    weekly2_country_rank_events_finished = models.IntegerField(null=True, blank=True)
    weekly2_country_rank_points = models.IntegerField(null=True, blank=True)
    weekly2_country_rank_average_points = models.IntegerField(null=True, blank=True)
    weekly2_country_rank_average_finish_place = models.IntegerField(null=True, blank=True)
    weekly2_country_rank_first_places = models.IntegerField(null=True, blank=True)
    weekly2_country_rank_top_3 = models.IntegerField(null=True, blank=True)
    weekly2_country_rank_top_10 = models.IntegerField(null=True, blank=True)
    weekly2_country_rank_top_100 = models.IntegerField(null=True, blank=True)
    weekly2_country_rank_driving_time_seconds = models.IntegerField(null=True, blank=True)

    monthly_country_rank_events_finished = models.IntegerField(null=True, blank=True)
    monthly_country_rank_points = models.IntegerField(null=True, blank=True)
    monthly_country_rank_average_points = models.IntegerField(null=True, blank=True)
    monthly_country_rank_average_finish_place = models.IntegerField(null=True, blank=True)
    monthly_country_rank_first_places = models.IntegerField(null=True, blank=True)
    monthly_country_rank_top_3 = models.IntegerField(null=True, blank=True)
    monthly_country_rank_top_10 = models.IntegerField(null=True, blank=True)
    monthly_country_rank_top_100 = models.IntegerField(null=True, blank=True)
    monthly_country_rank_driving_time_seconds = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.player_id)
    class Meta:
        ordering = ['player_id']


# Database table for all unique players info.
class CountriesInfo(models.Model):
    country_name = models.CharField(max_length=50)

    overall_number_of_drivers = models.IntegerField()
    overall_events_finished = models.IntegerField()
    overall_average_finish_place = models.FloatField()
    overall_first_places = models.IntegerField()
    overall_top_3 = models.IntegerField()
    overall_top_10 = models.IntegerField()
    overall_top_100 = models.IntegerField()
    overall_driving_time_seconds = models.FloatField()
    overall_points = models.IntegerField()
    overall_average_points = models.IntegerField()

    daily_number_of_drivers = models.IntegerField()
    daily_events_finished = models.IntegerField()
    daily_average_finish_place = models.FloatField()
    daily_first_places = models.IntegerField()
    daily_top_3 = models.IntegerField()
    daily_top_10 = models.IntegerField()
    daily_top_100 = models.IntegerField()
    daily_driving_time_seconds = models.FloatField()
    daily_points = models.IntegerField()
    daily_average_points = models.IntegerField()

    daily2_number_of_drivers = models.IntegerField()
    daily2_events_finished = models.IntegerField()
    daily2_average_finish_place = models.FloatField()
    daily2_first_places = models.IntegerField()
    daily2_top_3 = models.IntegerField()
    daily2_top_10 = models.IntegerField()
    daily2_top_100 = models.IntegerField()
    daily2_driving_time_seconds = models.FloatField()
    daily2_points = models.IntegerField()
    daily2_average_points = models.IntegerField()

    weekly_number_of_drivers = models.IntegerField()
    weekly_events_finished = models.IntegerField()
    weekly_average_finish_place = models.FloatField()
    weekly_first_places = models.IntegerField()
    weekly_top_3 = models.IntegerField()
    weekly_top_10 = models.IntegerField()
    weekly_top_100 = models.IntegerField()
    weekly_driving_time_seconds = models.FloatField()
    weekly_points = models.IntegerField()
    weekly_average_points = models.IntegerField()

    weekly2_number_of_drivers = models.IntegerField()
    weekly2_events_finished = models.IntegerField()
    weekly2_average_finish_place = models.FloatField()
    weekly2_first_places = models.IntegerField()
    weekly2_top_3 = models.IntegerField()
    weekly2_top_10 = models.IntegerField()
    weekly2_top_100 = models.IntegerField()
    weekly2_driving_time_seconds = models.FloatField()
    weekly2_points = models.IntegerField()
    weekly2_average_points = models.IntegerField()

    monthly_number_of_drivers = models.IntegerField()
    monthly_events_finished = models.IntegerField()
    monthly_average_finish_place = models.FloatField()
    monthly_first_places = models.IntegerField()
    monthly_top_3 = models.IntegerField()
    monthly_top_10 = models.IntegerField()
    monthly_top_100 = models.IntegerField()
    monthly_driving_time_seconds = models.FloatField()
    monthly_points = models.IntegerField()
    monthly_average_points = models.IntegerField()

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
    no_country_name = models.CharField(max_length=100)

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
