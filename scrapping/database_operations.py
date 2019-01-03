"""This code is used for getting data to database with two steps through text files which have been web scraped before."""

from timeit import default_timer as timer
import os
import io

from .models import EventInfo, LeaderBoard, TotalUniqueDrivers, TotalQualifiedDrivers, NoCountryNameCheck, PlayersInfo,\
CountriesInfo, TotalQualifiedCountries, LastDatabaseUpdateTime, SiteUpdateStatus



def database_operations_execution_function():




    # START functions for changing messages in site during the database update.
    def site_update_status_function(message):
        site_update_status_obj = SiteUpdateStatus.objects.all()
        for i in site_update_status_obj:
            i.delete()

        site_update_status_object = SiteUpdateStatus()
        site_update_status_object.update_status = message
        site_update_status_object.save()
    # END functions for changing messages in site during the database update.




    site_update_status_function('Site Updating - Phase 1')




    print('Text file to database conversion started!')

    directory = os.path.dirname(__file__)

    folder_path = directory + os.path.sep + 'DirtRally_codes_for_web_scraping' + os.path.sep + 'Dirt_Rally_web_scraping_for_txt' + os.path.sep + 'Leaderboard_txt'
    folder_name_list = os.listdir(folder_path)   # == ['1. Daily', '2. Daily2', '3. Weekly', '4. Weekly2', '5. Monthly']




    """ code to delete all EventInfo and LeaderBoard entries."""
    # leaderb_delete_object = EventInfo.objects.all()
    # for i in leaderb_delete_object:
    #     i.delete()
    #     print('del')
    # print('deleted')
    # exit()
    """ code to delete all EventInfo and LeaderBoard entries."""




    time_control_1 = timer()

    # START of code for getting data to database.
    count_no_country_name = 0
    list_of_events_since_last_webscarping = []

    for event_folder_name in folder_name_list:
        path_to_text_files = folder_path + os.path.sep + event_folder_name
        event_list = os.listdir(path_to_text_files)  # == ['Daily_08.19.2018.txt', 'Daily_08.20.2018.txt', 'Daily_08.21.2018.txt', 'Daily_08.22.2018.txt', 'Daily_08.23.2018.txt', 'Daily_08.24.2018.txt', 'Daily_08.25.2018.txt', 'Daily_08.26.2018.txt', 'Daily_08.27.2018.txt']

        for event in event_list:

            db_search = list(EventInfo.objects.all())  # Queryset must be in list function. To avoid "remaining elements truncated".
            db_search_string = str(db_search)

            # Search database for already existing events. If not in database, add this event.
            if event.replace('.txt', '') in db_search_string:
                continue

            else:
                event_two_part_list = event.replace('.txt', '').split('_')    # variable 'event_two_part_list' type is list.
                list_of_events_since_last_webscarping.append(event_two_part_list)   # List of lists of events since last web scraping Under automated everyday scraping there will be one from each category (One daily, daily2, weekly, weekly2 and monthly.)

                textfile = io.open(path_to_text_files + os.path.sep + event, mode="r", encoding="utf-8")

                full_string = textfile.read()
                text_line_list = full_string.split('\n')


                event_category = text_line_list[0].split(': ')[1]
                date = text_line_list[1].split(': ')[1]
                event_name = text_line_list[2].split(': ')[1]
                event_location = text_line_list[3].split(': ')[1]
                stage_name = text_line_list[4].split(': ')[1]
                time_of_day = text_line_list[5].split(': ')[1]
                weather = text_line_list[6].split(': ')[1]
                number_of_drivers = text_line_list[8].split(': ')[1]

                # For weekly monthly event without location and weather date. Replace 'None' with 'Empty'.
                if event_location == 'None':
                    event_location = 'Empty'
                if stage_name == 'None':
                    stage_name = 'Empty'
                if time_of_day == 'None':
                    time_of_day = 'Empty'
                if weather == 'None':
                    weather = 'Empty'

                print(event_category)
                print(date)
                print(event_name)
                print(event_location)
                print(stage_name)
                print(time_of_day)
                print(weather)
                print(number_of_drivers, '\n')

                leaderb_list = full_string.split('Leaderboard: ')
                full_leaderb_string = leaderb_list[1].replace("[(", "").replace(")]", "")


                # Extract individual driver information strings.
                listy_a = full_leaderb_string.split('), (')
                listy_a = [x for x in listy_a if len(x) > 50]


                tuple_list = []
                for j in listy_a:
                    print(j)

                    k = j.replace('"', "'")
                    listy_c = k.split("', '")
                    listy_d = []

                    for g in listy_c:
                        if g[0] == "'" or g[-1] == "'":
                            v = g.replace("'", "")
                            listy_d.append(v)
                        else:
                            listy_d.append(g)

                    tuple_list.append(tuple(listy_d))


                event_info_object = EventInfo()
                event_info_object.event_category = event_category
                event_info_object.date = date
                event_info_object.event_name = event_name
                event_info_object.location = event_location
                event_info_object.stage = stage_name
                event_info_object.time_of_the_day = time_of_day
                event_info_object.weather = weather
                event_info_object.total_drivers = number_of_drivers
                event_info_object.save()

                for i in range(int(number_of_drivers)):
                    leaderboard_object = LeaderBoard()
                    leaderboard_object.event_info = event_info_object
                    leaderboard_object.position = int(tuple_list[i][0])
                    if tuple_list[i][1] == 'NO COUNTRY':
                        count_no_country_name += 1
                    leaderboard_object.country_name = tuple_list[i][1]
                    leaderboard_object.name = tuple_list[i][2]
                    leaderboard_object.vehicle = tuple_list[i][3]
                    leaderboard_object.time = tuple_list[i][4]
                    leaderboard_object.time_seconds = float(tuple_list[i][5])
                    leaderboard_object.diff_1st = tuple_list[i][6]
                    leaderboard_object.player_id = int(tuple_list[i][7])
                    leaderboard_object.save()

    print('count_no_country_name = ', count_no_country_name)

    print('Text file to database conversion completed!')
    # END of code for getting data to database.














    # START functions for converting drivers time from seconds to time string h m s.
    def time_h_m_s_converter(input_time):
        hours = 0
        minutes = 0

        if input_time < 3600:
            minutes = input_time // 60
            seconds = input_time % 60

        elif input_time < 60:
            seconds = input_time

        else:
            hours = input_time // 3600
            remainder = input_time % 3600
            if remainder < 60:
                seconds = remainder
            else:
                minutes = remainder // 60
                seconds = remainder % 60

        time_format = str(int(hours)) + 'h ' + str(int(minutes)) + 'm ' + '{0:.3f}'.format(
            round(seconds, 3)) + 's'

        return time_format

    # END functions for converting drivers time from seconds to time string h m s.










    # START of code for creating list of playerIDs from last web scraping session.
    print('Amount of new events since last scrapping: ', len(list_of_events_since_last_webscarping))
    player_id_list_for_last_scraping = []
    for i in list_of_events_since_last_webscarping:

        obj = LeaderBoard.objects.filter(event_info__event_category__exact=i[0], event_info__date__exact=i[1])


        for k in obj:
            if k.player_id in player_id_list_for_last_scraping:
                continue
            else:
                player_id_list_for_last_scraping.append(k.player_id)

    print('Amount of participated player IDs since last scrapping: ', len(player_id_list_for_last_scraping))
    # END of code for creating list of playerIDs from last web scraping session.








    # START of function for finding last driven event's date for each driver.
    def find_last_date(event_info_list):
        flipped_dates_list = []
        for itering in event_info_list:
            flipped_year_list = []
            date_separated_list = itering.split('.')
            flipped_year_list.append(date_separated_list[2])
            flipped_year_list.append(date_separated_list[0])
            flipped_year_list.append(date_separated_list[1])

            flipped_dates_list.append('.'.join(flipped_year_list))

        sorted_date_list = sorted(flipped_dates_list)

        last_date = sorted_date_list[-1]

        last_date_list = last_date.split('.')

        last_date_correct = []
        last_date_correct.append(last_date_list[1])
        last_date_correct.append(last_date_list[2])
        last_date_correct.append(last_date_list[0])

        fliped_correct_last_date = []
        fliped_correct_last_date.append('.'.join(last_date_correct))

        return fliped_correct_last_date[0]
    # END of function for finding last driven event's date for each driver.




















    site_update_status_function('Site Updating - Phase 2')

    time_control_2 = timer()

    #TODO: !!!!!!!!!!!!!!!!!!WARNING: Remember to comment out one of the PlayerInfo database codes versions!!!!!!!!!!!!!!!!!!





    # #TODO: Version 1. Automated PlayerInfo.
    #
    # # ******************************Launch this code if web scraping is already automated (web page is in production mode).
    # # START of code for getting all unique players info to database PlayersInfo.
    # # This code gets every PlayerID from all database leaderboards and corresponding player info.
    #
    # """Delete PlayerInfo database every time before starting to write new one."""
    # player_id_delete_object = PlayersInfo.objects.all()
    # for i in player_id_delete_object:
    #     if i.player_id in player_id_list_for_last_scraping:
    #         i.delete()
    # print('Old PlayerInfo entries deleted!')
    # """Delete PlayerInfo database every time before starting to write new one."""
    #
    #
    # time_control_3 = timer()
    #
    #
    # print('Starting new PlayersInfo database!')
    # playerinfo_nr = 0
    # for last_scraping_playerid in player_id_list_for_last_scraping:
    #
    #     leaderb_obj = LeaderBoard.objects.filter(player_id__exact=last_scraping_playerid)
    #
    #     events_finished_count = 0
    #     sum_of_finish_places = 0
    #     first_places_count = 0
    #     top_3_count = 0
    #     top_10_count = 0
    #     top_100_count = 0
    #     total_driving_time_count = 0
    #
    #     event_info_date_list = []
    #     for k in leaderb_obj:
    #
    #         event_info_date_list.append(k.event_info.date)
    #
    #         events_finished_count += 1
    #
    #         if k.position == 1:
    #             first_places_count += 1
    #
    #         if k.position <= 3:
    #             top_3_count += 1
    #
    #         if k.position <= 10:
    #             top_10_count += 1
    #
    #         if k.position <= 100:
    #             top_100_count += 1
    #
    #         sum_of_finish_places += k.position
    #         total_driving_time_count += k.time_seconds
    #
    #         percent_1st_place_calc = round(first_places_count / events_finished_count * 100, 2)
    #         percent_top_3_calc = round(top_3_count / events_finished_count * 100, 2)
    #         percent_top_10_calc = round(top_10_count / events_finished_count * 100, 2)
    #         percent_top_100_calc = round(top_100_count / events_finished_count * 100, 2)
    #
    #
    #         # START Code: Find driver's latest name and country.
    #         obj = LeaderBoard.objects.filter(event_info__date__exact=find_last_date(event_info_date_list),
    #                                          player_id__exact=last_scraping_playerid)
    #
    #         country = ''
    #         name = ''
    #         for m in obj:
    #             country = m.country_name
    #             name = m.name
    #             break
    #         # END Code: Find driver's latest name and country.
    #
    #
    #
    #     if events_finished_count >= 3:    # This line limits top table to drivers who have finished certain number on events. For example: at least 3
    #
    #         player_id_object = PlayersInfo()
    #
    #         player_id_object.country_from = country
    #         player_id_object.name = name
    #         player_id_object.player_id = last_scraping_playerid
    #         player_id_object.events_finished = events_finished_count
    #         player_id_object.average_finish_place = round(float(sum_of_finish_places) / events_finished_count, 1)
    #         player_id_object.first_places = first_places_count
    #         player_id_object.top_3 = top_3_count
    #         player_id_object.top_10 = top_10_count
    #         player_id_object.top_100 = top_100_count
    #         player_id_object.percentile_1st_place = percent_1st_place_calc
    #         player_id_object.percentile_top_3 = percent_top_3_calc
    #         player_id_object.percentile_top_10 = percent_top_10_calc
    #         player_id_object.percentile_top_100 = percent_top_100_calc
    #         player_id_object.total_driving_time_seconds = round(total_driving_time_count, 3)
    #         player_id_object.total_driving_time_string = time_h_m_s_converter(total_driving_time_count)
    #
    #         playerinfo_nr += 1
    #         print(playerinfo_nr)
    #
    #         player_id_object.save()
    #
    # print('New PlayerInfo database completed!')
    #
    # # END of code for getting all unique players info to database PlayersInfo.
    # # ******************************Launch this code if web scraping is already automated (web page is in production mode).












    # TODO: Version 2. Non-Automated PlayerInfo.

    # ******************************Launch this code if web scraping is already not automated or database is not fully uploaded.
    # START of code for getting all unique players info to database PlayersInfo.
    # This code gets every PlayerID from all database leaderboards and corresponding player info.

    """Delete PlayerInfo database every time before starting to write new one."""
    try:
        player_id_delete_object = PlayersInfo.objects.all()
        for i in player_id_delete_object:
            i.delete()
        print('Old PlayerInfo entries deleted!')
    except:
        print('PlayerInfo database was already empty!')
    """Delete PlayerInfo database every time before starting to write new one."""

    time_control_3 = timer()

    print('Starting new PlayersInfo database!')
    player_id_database_list = []
    player_id_obj = LeaderBoard.objects.all()

    count_to_stop = 0
    playerinfo_nr = 0
    for i in player_id_obj:

        # # Start. Code for controlling how many values will be saved to database. For testing purposes.
        # count_to_stop += 1
        # if count_to_stop == 1000:
        #     break
        # # End. Code for controlling how many values will be saved to database. For testing purposes.

        if i.player_id in player_id_database_list:
            continue

        else:
            player_id_database_list.append(i.player_id)  # Equal to TotalUniqueDrivers value.

            leaderb_obj = LeaderBoard.objects.filter(player_id__exact=i.player_id)

            event_info_date_list = []
            events_finished_count = 0
            sum_of_finish_places = 0
            first_places_count = 0
            top_3_count = 0
            top_10_count = 0
            top_100_count = 0
            total_driving_time_count = 0
            for k in leaderb_obj:
                event_info_date_list.append(k.event_info.date)

                events_finished_count += 1

                if k.position == 1:
                    first_places_count += 1

                if k.position <= 3:
                    top_3_count += 1

                if k.position <= 10:
                    top_10_count += 1

                if k.position <= 100:
                    top_100_count += 1

                sum_of_finish_places += k.position
                total_driving_time_count += k.time_seconds

            percent_1st_place_calc = round(first_places_count / events_finished_count * 100, 2)
            percent_top_3_calc = round(top_3_count / events_finished_count * 100, 2)
            percent_top_10_calc = round(top_10_count / events_finished_count * 100, 2)
            percent_top_100_calc = round(top_100_count / events_finished_count * 100, 2)



            # START Code: Find driver's latest name and country.
            obj = LeaderBoard.objects.filter(event_info__date__exact=find_last_date(event_info_date_list),
                                             player_id__exact=i.player_id)

            country = ''
            name = ''
            for m in obj:
                country = m.country_name
                name = m.name
                break
            # END Code: Find driver's latest name and country.



            if events_finished_count >= 3:    # This line limits top table to drivers who have finished certain number on events. For example: at least 3

                player_id_object = PlayersInfo()

                player_id_object.country_from = country
                player_id_object.name = name
                player_id_object.player_id = i.player_id
                player_id_object.events_finished = events_finished_count
                player_id_object.average_finish_place = round(float(sum_of_finish_places) / events_finished_count, 1)
                player_id_object.first_places = first_places_count
                player_id_object.top_3 = top_3_count
                player_id_object.top_10 = top_10_count
                player_id_object.top_100 = top_100_count
                player_id_object.percentile_1st_place = percent_1st_place_calc
                player_id_object.percentile_top_3 = percent_top_3_calc
                player_id_object.percentile_top_10 = percent_top_10_calc
                player_id_object.percentile_top_100 = percent_top_100_calc
                player_id_object.total_driving_time_seconds = round(total_driving_time_count, 3)
                player_id_object.total_driving_time_string = time_h_m_s_converter(total_driving_time_count)

                playerinfo_nr += 1
                print(playerinfo_nr)

                player_id_object.save()

    print('New PlayerInfo database completed!')
    # END of code for getting all unique players info to database PlayersInfo.

    # ******************************Launch this code if web scraping is already not automated or database is not fully uploaded.





    #TODO: !!!!!!!!!!!!!!!!!!WARNING: Remember to comment out one of the PlayerInfo database codes version!!!!!!!!!!!!!!!!!!















    time_control_4 = timer()

    """Code for writing TotalUniqueDrivers database entry."""
    player_id_obj = LeaderBoard.objects.all()

    player_id_database_list = []
    for i in player_id_obj:
        if i.player_id in player_id_database_list:
            continue
        else:
            player_id_database_list.append(i.player_id)

    total_unique_drivers_object = TotalUniqueDrivers()
    total_unique_drivers_object.player_id_list_len = len(player_id_database_list)
    total_unique_drivers_object.save()
    """Code for writing TotalUniqueDrivers database entry."""


    """Code for writing TotalQualifiedDrivers database entry."""
    players_info_obj = PlayersInfo.objects.all()

    total_top_qualified_drivers = 0
    for i in players_info_obj:
        total_top_qualified_drivers += 1

    total_top_qualified_drivers_object = TotalQualifiedDrivers()
    total_top_qualified_drivers_object.qualified_drivers = total_top_qualified_drivers
    total_top_qualified_drivers_object.save()
    """Code for writing TotalQualifiedDrivers database entry."""

    time_control_5 = timer()










    # START of code for saving NO COUNTRY results on database.
    # This code is for me to check database to see if player has been uploaded on database with unknown country.
    no_country_object = LeaderBoard.objects.filter(country_name__exact='NO COUNTRY')

    no_country_count = 0
    for i in no_country_object:
        no_country_count += 1

    count_no_country_name_object = NoCountryNameCheck()
    count_no_country_name_object.no_country_name = no_country_count
    count_no_country_name_object.save()
    # END of code for saving NO COUNTRY results on database.





    time_control_6 = timer()

    # START of code for getting all countries info to database CountriesInfo.
    # This code gets every qualified driver from PlayersInfo and adds them together.

    """Delete CountriesInfo database every time before starting to write new one."""
    countriesinfo_delete_object = CountriesInfo.objects.all()
    for i in countriesinfo_delete_object:
        i.delete()
    print('Old CountriesInfo entries deleted!')
    """Delete CountriesInfo database every time before starting to write new one."""


    print('Starting new CountriesInfo database!')
    players_info_obj = PlayersInfo.objects.all()

    country_list = []
    for i in players_info_obj:
        if i.country_from in country_list:
            continue
        else:
            country_list.append(i.country_from)

    for i in country_list:
        players_info_country_obj = PlayersInfo.objects.filter(country_from__exact=i)


        number_of_drivers_count = 0
        events_finished_count = 0
        average_finish_place_sum = 0
        first_places_count = 0
        top_3_count = 0
        top_10_count = 0
        top_100_count= 0
        total_driving_time_count = 0

        for j in players_info_country_obj:
            number_of_drivers_count += 1
            events_finished_count += j.events_finished
            average_finish_place_sum += j.average_finish_place
            first_places_count += j.first_places
            top_3_count += j.top_3
            top_10_count += j.top_10
            top_100_count += j.top_100
            total_driving_time_count += j.total_driving_time_seconds

        percent_1st_place_calc = round(first_places_count / events_finished_count * 100, 2)
        percent_top_3_calc = round(top_3_count / events_finished_count * 100, 2)
        percent_top_10_calc = round(top_10_count / events_finished_count * 100, 2)
        percent_top_100_calc = round(top_100_count / events_finished_count * 100, 2)


        countriesinfo_object = CountriesInfo()

        countriesinfo_object.number_of_drivers = number_of_drivers_count
        countriesinfo_object.country_name = i
        countriesinfo_object.events_finished = events_finished_count
        countriesinfo_object.average_finish_place = round(average_finish_place_sum / number_of_drivers_count, 1)
        countriesinfo_object.first_places = first_places_count
        countriesinfo_object.top_3 = top_3_count
        countriesinfo_object.top_10 = top_10_count
        countriesinfo_object.top_100 = top_100_count
        countriesinfo_object.percentile_1st_place = percent_1st_place_calc
        countriesinfo_object.percentile_top_3 = percent_top_3_calc
        countriesinfo_object.percentile_top_10 = percent_top_10_calc
        countriesinfo_object.percentile_top_100 = percent_top_100_calc
        countriesinfo_object.total_driving_time_seconds = round(total_driving_time_count, 3)
        countriesinfo_object.total_driving_time_string = time_h_m_s_converter(total_driving_time_count)

        countriesinfo_object.save()


    """Code for writing TotalQualifiedCountries database entry."""
    total_top_qualified_countries_object = TotalQualifiedCountries()
    total_top_qualified_countries_object.qualified_countries = len(country_list)
    total_top_qualified_countries_object.save()
    """Code for writing TotalQualifiedCountries database entry."""
    # END of code for getting all countries info to database CountriesInfo.

    time_control_7 = timer()







    # START code for Last database update time and total days since database active.
    import datetime

    utc = datetime.datetime.utcnow()
    utc_time_string = utc.strftime("%m.%d.%Y  %H:%M")

    utc_time_string_to_list = utc_time_string.split('  ')
    date_list = utc_time_string_to_list[0].split('.')
    day_list = list(date_list[1])

    if int(day_list[0]) == 0:
        date_days = day_list[1]
    else:
        date_days = date_list[1]

    d0 = datetime.date(2018, 7, 27)
    d1 = datetime.date(int(date_list[2]), int(date_list[0]), int(date_days))
    delta = d1 - d0

    last_database_update_time_object = LastDatabaseUpdateTime()
    last_database_update_time_object.last_database_update_time = utc_time_string
    last_database_update_time_object.days_database_active = delta.days
    last_database_update_time_object.save()
    # END code for Last database update time and total days since database active.

    site_update_status_obj = SiteUpdateStatus.objects.all()
    for i in site_update_status_obj:
        i.delete()




    delta_time_all = time_control_7 - time_control_1

    print('Web Scrapping time: ', time_control_2 - time_control_1)
    print('PlayersInfo delete database time: ', time_control_3 - time_control_2)
    print('PlayersInfo new database time: ', time_control_4 - time_control_3)
    print('Total Drivers database: ', time_control_5 - time_control_4)
    print('CountriesInfo new database time: ', time_control_7 - time_control_6)

    print('Total script time: ', delta_time_all)




