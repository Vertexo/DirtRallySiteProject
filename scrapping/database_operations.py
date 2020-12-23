"""This code is used for getting data to database with two steps through text files which have been web scraped before."""

from timeit import default_timer as timer
import sys
import os
import io
from django.db.models import Q

from .models import EventInfo, LeaderBoard, TotalUniqueDrivers, TotalQualifiedDrivers, NoCountryNameCheck, PlayersInfo,\
CountriesInfo, TotalQualifiedCountries, LastDatabaseUpdateTime, SiteUpdateStatus



def database_operations_execution_function():




    # START function for changing messages in site during the database update.
    def site_update_status_function(message):
        site_update_status_obj = SiteUpdateStatus.objects.all()
        for i in site_update_status_obj:
            i.delete()

        site_update_status_object = SiteUpdateStatus()
        site_update_status_object.update_status = message
        site_update_status_object.save()
    # END function for changing messages in site during the database update.





    # START of function for calculating event points by category.
    # Point calculation formulas are taken from excel file "Dirt Rally event point scoring examples".
    def points_calculation_func(total_drivers, position, category):

        base_points_list = [1]
        top_10_daily_base_points = [400, 440, 490, 550, 620, 700, 790, 1000, 1200, 1500]
        a = 1
        for _ in range(1, 90):
            a = 3 + a
            base_points_list.append(a)
        for i in top_10_daily_base_points:
            base_points_list.append(i)

        base_points_list = base_points_list[::-1]

        if category == 'Daily' or category == 'Daily2':
            base_points = 0
            if position <= 100:
                base_points = base_points_list[position - 1]

            # print(base_points)
            position_points = (total_drivers - position) - (position - 1)
            # print(position_points)
            total_points = base_points + position_points

            return total_points


        elif category == 'Weekly' or category == 'Weekly2':
            base_points = 0
            if position <= 100:
                base_points = base_points_list[position - 1] * 2

            # print(base_points)
            position_points = (total_drivers - position) + 100
            # print(position_points)
            total_points = base_points + position_points

            return total_points


        elif category == 'Monthly':
            base_points = 0
            if position <= 100:
                base_points = base_points_list[position - 1] * 3

            # print(base_points)
            position_points = (total_drivers - position) + 300
            # print(position_points)
            total_points = base_points + position_points

            return total_points
    # END of function for calculating event points by category.












    """ code to delete all EventInfo and LeaderBoard entries."""
    # # This section of code is usually commented out under normal conditions.
    # leaderb_delete_object = EventInfo.objects.all()  # LeaderBoard table will also be deleted. It is joined with EventInfo tabel through foreign ID and have a parameter on_delete=models.CASCADE in models.py.
    # for i in leaderb_delete_object:
    #     i.delete()
    #     print('EventInfo item deleted')

    # # Delete PlayersInfo as well.
    # player_id_delete_object = PlayersInfo.objects.all() 
    # for i in player_id_delete_object:
    #     i.delete()
    #     print('PlayersInfo item deleted')
    # print('Finished')

    # exit()  # After finished, terminate the whole operation (file).
    """ code to delete all EventInfo and LeaderBoard entries."""










    site_update_status_function('Site Update - Collecting data')


    # LOGS_1
    stdout_1 = sys.stdout
    log_file_1 = open("log_file.log", "a")
    sys.stdout = log_file_1
    # LOGS_1
    print('Text file to database conversion started!')
    # LOGS_1
    sys.stdout = stdout_1
    log_file_1.close()
    # LOGS_1

    directory = os.path.dirname(__file__)

    folder_path = directory + os.path.sep + 'DirtRally_codes_for_web_scraping' + os.path.sep + 'Dirt_Rally_web_scraping_for_txt' + os.path.sep + 'Leaderboard_txt'
    folder_name_list = os.listdir(folder_path)   # == ['1. Daily', '2. Daily2', '3. Weekly', '4. Weekly2', '5. Monthly']









    # timer
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
                list_of_events_since_last_webscarping.append(event_two_part_list)   # List of lists of events since last web scraping Under automated everyday scraping, there will be one from each category (One daily, daily2, weekly, weekly2 and monthly.)

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


                # LOGS_2
                stdout_2 = sys.stdout
                log_file_2 = open("log_file.log", "a")
                sys.stdout = log_file_2
                # LOGS_2
                print(event_category)
                print(date)
                print(event_name)
                print(event_location)
                print(stage_name)
                print(time_of_day)
                print(weather)
                print(number_of_drivers, '\n')
                # LOGS_2
                sys.stdout = stdout_2
                log_file_2.close()
                # LOGS_2

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
                    leaderboard_object.earned_points = points_calculation_func(int(number_of_drivers), int(tuple_list[i][0]), event_category)
                    leaderboard_object.save()


    # LOGS_3
    stdout_3 = sys.stdout
    log_file_3 = open("log_file.log", "a")
    sys.stdout = log_file_3
    # LOGS_3
    print('count_no_country_name = ', count_no_country_name)

    print('Text file to database conversion completed!')
    # END of code for getting data to database.

    













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
    
    # LOGS_3
    sys.stdout = stdout_3
    log_file_3.close()
    # LOGS_3





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













    site_update_status_function('Site Update - Leaderboards')

    # timer
    time_control_2 = timer()




    #NOTE: !!!!!!!!!!!!!!!!!!WARNING: Remember to comment out one of the PlayerInfo database codes versions!!!!!!!!!!!!!!!!!!





    #NOTE: Version 1. Automated PlayerInfo.

    # ******************************Launch this code if web scraping is already automated (web page is in production mode).
    # START of code for getting all unique players info to database PlayersInfo.
    # This code gets every PlayerID from all database leaderboards and corresponding player info.

    # LOGS_4
    stdout_4 = sys.stdout
    log_file_4 = open("log_file.log", "a")
    sys.stdout = log_file_4
    # LOGS_4
    """Deletes PlayerInfo database every time before starting to write new one."""
    player_id_delete_object = PlayersInfo.objects.all()
    deleted_count = 0
    for i in player_id_delete_object:
        if i.player_id in player_id_list_for_last_scraping:
            i.delete()
            deleted_count += 1
            print(deleted_count)
    print('Old PlayerInfo entries deleted!')
    """Deletes PlayerInfo database every time before starting to write new one."""

    # timer
    time_control_3 = timer()


    print('Starting new PlayersInfo database! !!!Collects only qualified drivers!!!')
    # LOGS_4
    sys.stdout = stdout_4
    log_file_4.close()
    # LOGS_4


    playerinfo_nr = 0
    for last_scraping_playerid in player_id_list_for_last_scraping:

        leaderb_obj = LeaderBoard.objects.filter(player_id__exact=last_scraping_playerid, event_info__event_category__exact='Daily')

        daily_events_finished_count = 0
        daily_sum_of_finish_places = 0
        daily_first_places_count = 0
        daily_top_3_count = 0
        daily_top_10_count = 0
        daily_top_100_count = 0
        daily_driving_time_count = 0
        daily_points_count = 0

        for k in leaderb_obj:
            daily_events_finished_count += 1
            if k.position == 1:
                daily_first_places_count += 1
            if k.position <= 3:
                daily_top_3_count += 1
            if k.position <= 10:
                daily_top_10_count += 1
            if k.position <= 100:
                daily_top_100_count += 1

            daily_sum_of_finish_places += k.position
            daily_driving_time_count += k.time_seconds
            daily_points_count += k.earned_points


        leaderb_obj = LeaderBoard.objects.filter(player_id__exact=last_scraping_playerid, event_info__event_category__exact='Daily2')

        daily2_events_finished_count = 0
        daily2_sum_of_finish_places = 0
        daily2_first_places_count = 0
        daily2_top_3_count = 0
        daily2_top_10_count = 0
        daily2_top_100_count = 0
        daily2_driving_time_count = 0
        daily2_points_count = 0

        for k in leaderb_obj:
            daily2_events_finished_count += 1
            if k.position == 1:
                daily2_first_places_count += 1
            if k.position <= 3:
                daily2_top_3_count += 1
            if k.position <= 10:
                daily2_top_10_count += 1
            if k.position <= 100:
                daily2_top_100_count += 1

            daily2_sum_of_finish_places += k.position
            daily2_driving_time_count += k.time_seconds
            daily2_points_count += k.earned_points


        leaderb_obj = LeaderBoard.objects.filter(player_id__exact=last_scraping_playerid, event_info__event_category__exact='Weekly')

        weekly_events_finished_count = 0
        weekly_sum_of_finish_places = 0
        weekly_first_places_count = 0
        weekly_top_3_count = 0
        weekly_top_10_count = 0
        weekly_top_100_count = 0
        weekly_driving_time_count = 0
        weekly_points_count = 0

        for k in leaderb_obj:
            weekly_events_finished_count += 1
            if k.position == 1:
                weekly_first_places_count += 1
            if k.position <= 3:
                weekly_top_3_count += 1
            if k.position <= 10:
                weekly_top_10_count += 1
            if k.position <= 100:
                weekly_top_100_count += 1

            weekly_sum_of_finish_places += k.position
            weekly_driving_time_count += k.time_seconds
            weekly_points_count += k.earned_points


        leaderb_obj = LeaderBoard.objects.filter(player_id__exact=last_scraping_playerid, event_info__event_category__exact='Weekly2')

        weekly2_events_finished_count = 0
        weekly2_sum_of_finish_places = 0
        weekly2_first_places_count = 0
        weekly2_top_3_count = 0
        weekly2_top_10_count = 0
        weekly2_top_100_count = 0
        weekly2_driving_time_count = 0
        weekly2_points_count = 0

        for k in leaderb_obj:
            weekly2_events_finished_count += 1
            if k.position == 1:
                weekly2_first_places_count += 1
            if k.position <= 3:
                weekly2_top_3_count += 1
            if k.position <= 10:
                weekly2_top_10_count += 1
            if k.position <= 100:
                weekly2_top_100_count += 1

            weekly2_sum_of_finish_places += k.position
            weekly2_driving_time_count += k.time_seconds
            weekly2_points_count += k.earned_points


        leaderb_obj = LeaderBoard.objects.filter(player_id__exact=last_scraping_playerid, event_info__event_category__exact='Monthly')

        monthly_events_finished_count = 0
        monthly_sum_of_finish_places = 0
        monthly_first_places_count = 0
        monthly_top_3_count = 0
        monthly_top_10_count = 0
        monthly_top_100_count = 0
        monthly_driving_time_count = 0
        monthly_points_count = 0

        for k in leaderb_obj:
            monthly_events_finished_count += 1
            if k.position == 1:
                monthly_first_places_count += 1
            if k.position <= 3:
                monthly_top_3_count += 1
            if k.position <= 10:
                monthly_top_10_count += 1
            if k.position <= 100:
                monthly_top_100_count += 1

            monthly_sum_of_finish_places += k.position
            monthly_driving_time_count += k.time_seconds
            monthly_points_count += k.earned_points


        overall_events_finished_count = daily_events_finished_count + daily2_events_finished_count + weekly_events_finished_count + weekly2_events_finished_count + monthly_events_finished_count
        overall_sum_of_finish_places = daily_sum_of_finish_places + daily2_sum_of_finish_places + weekly_sum_of_finish_places + weekly2_sum_of_finish_places + monthly_sum_of_finish_places
        overall_first_places_count = daily_first_places_count + daily2_first_places_count + weekly_first_places_count + weekly2_first_places_count + monthly_first_places_count
        overall_top_3_count = daily_top_3_count + daily2_top_3_count + weekly_top_3_count + weekly2_top_3_count + monthly_top_3_count
        overall_top_10_count = daily_top_10_count + daily2_top_10_count + weekly_top_10_count + weekly2_top_10_count + monthly_top_10_count
        overall_top_100_count = daily_top_100_count + daily2_top_100_count + weekly_top_100_count + weekly2_top_100_count + monthly_top_100_count
        overall_driving_time_count = daily_driving_time_count + daily2_driving_time_count + weekly_driving_time_count + weekly2_driving_time_count + monthly_driving_time_count
        overall_points_count = daily_points_count + daily2_points_count + weekly_points_count + weekly2_points_count + monthly_points_count



        # Make obj just for getting last driven event date list.
        leaderb_obj = LeaderBoard.objects.filter(player_id__exact=last_scraping_playerid)

        event_info_date_list = []
        for k in leaderb_obj:
            event_info_date_list.append(k.event_info.date)
        # Make obj just for getting last driven event date list.

        # START Code: Find driver's latest name and country.
        obj = LeaderBoard.objects.filter(event_info__date__exact=find_last_date(event_info_date_list), player_id__exact=last_scraping_playerid)

        country = ''
        name = ''
        for m in obj:
            country = m.country_name
            name = m.name
            break
        # END Code: Find driver's latest name and country.



        if overall_events_finished_count >= 3:    # This line limits top table to drivers who have finished certain number on events. For example: at least 3

            # In this list add the Ids of the obvious cheaters to filter them out from PlayersInfo table. Skips to the next For-Loop iteration.
            # Potential cheaters: 1748070,
            cheatersIDList = [2094692, 1691289, 1155845]
            if last_scraping_playerid in cheatersIDList:
                print('Skipped cheater with ID: ', last_scraping_playerid)
                continue


            player_id_object = PlayersInfo()

            player_id_object.country_from = country
            player_id_object.name = name
            player_id_object.player_id = last_scraping_playerid

            player_id_object.overall_events_finished = overall_events_finished_count
            player_id_object.overall_average_finish_place = round(float(overall_sum_of_finish_places) / overall_events_finished_count, 1)
            player_id_object.overall_first_places = overall_first_places_count
            player_id_object.overall_top_3 = overall_top_3_count
            player_id_object.overall_top_10 = overall_top_10_count
            player_id_object.overall_top_100 = overall_top_100_count
            player_id_object.overall_driving_time_seconds = round(overall_driving_time_count, 3)
            player_id_object.overall_points = overall_points_count
            player_id_object.overall_average_points = round(float(overall_points_count) / overall_events_finished_count, 1)

            player_id_object.daily_events_finished = daily_events_finished_count
            if daily_events_finished_count != 0:
                player_id_object.daily_average_finish_place = round(float(daily_sum_of_finish_places) / daily_events_finished_count, 1)
                player_id_object.daily_average_points = round(float(daily_points_count) / daily_events_finished_count, 1)
            else:
                player_id_object.daily_average_finish_place = 0
                player_id_object.daily_average_points = 0
            player_id_object.daily_first_places = daily_first_places_count
            player_id_object.daily_top_3 = daily_top_3_count
            player_id_object.daily_top_10 = daily_top_10_count
            player_id_object.daily_top_100 = daily_top_100_count
            player_id_object.daily_driving_time_seconds = round(daily_driving_time_count, 3)
            player_id_object.daily_points = daily_points_count

            player_id_object.daily2_events_finished = daily2_events_finished_count
            if daily2_events_finished_count != 0:
                player_id_object.daily2_average_finish_place = round(float(daily2_sum_of_finish_places) / daily2_events_finished_count, 1)
                player_id_object.daily2_average_points = round(float(daily2_points_count) / daily2_events_finished_count, 1)
            else:
                player_id_object.daily2_average_finish_place = 0
                player_id_object.daily2_average_points = 0
            player_id_object.daily2_first_places = daily2_first_places_count
            player_id_object.daily2_top_3 = daily2_top_3_count
            player_id_object.daily2_top_10 = daily2_top_10_count
            player_id_object.daily2_top_100 = daily2_top_100_count
            player_id_object.daily2_driving_time_seconds = round(daily2_driving_time_count, 3)
            player_id_object.daily2_points = daily2_points_count

            player_id_object.weekly_events_finished = weekly_events_finished_count
            if weekly_events_finished_count != 0:
                player_id_object.weekly_average_finish_place = round(float(weekly_sum_of_finish_places) / weekly_events_finished_count, 1)
                player_id_object.weekly_average_points = round(float(weekly_points_count) / weekly_events_finished_count, 1)
            else:
                player_id_object.weekly_average_finish_place = 0
                player_id_object.weekly_average_points = 0
            player_id_object.weekly_first_places = weekly_first_places_count
            player_id_object.weekly_top_3 = weekly_top_3_count
            player_id_object.weekly_top_10 = weekly_top_10_count
            player_id_object.weekly_top_100 = weekly_top_100_count
            player_id_object.weekly_driving_time_seconds = round(weekly_driving_time_count, 3)
            player_id_object.weekly_points = weekly_points_count

            player_id_object.weekly2_events_finished = weekly2_events_finished_count
            if weekly2_events_finished_count != 0:
                player_id_object.weekly2_average_finish_place = round(float(weekly2_sum_of_finish_places) / weekly2_events_finished_count, 1)
                player_id_object.weekly2_average_points = round(float(weekly2_points_count) / weekly2_events_finished_count, 1)
            else:
                player_id_object.weekly2_average_finish_place = 0
                player_id_object.weekly2_average_points = 0
            player_id_object.weekly2_first_places = weekly2_first_places_count
            player_id_object.weekly2_top_3 = weekly2_top_3_count
            player_id_object.weekly2_top_10 = weekly2_top_10_count
            player_id_object.weekly2_top_100 = weekly2_top_100_count
            player_id_object.weekly2_driving_time_seconds = round(weekly2_driving_time_count, 3)
            player_id_object.weekly2_points = weekly2_points_count

            player_id_object.monthly_events_finished = monthly_events_finished_count
            if monthly_events_finished_count != 0:
                player_id_object.monthly_average_finish_place = round(float(monthly_sum_of_finish_places) / monthly_events_finished_count, 1)
                player_id_object.monthly_average_points = round(float(monthly_points_count) / monthly_events_finished_count, 1)
            else:
                player_id_object.monthly_average_finish_place = 0
                player_id_object.monthly_average_points = 0
            player_id_object.monthly_first_places = monthly_first_places_count
            player_id_object.monthly_top_3 = monthly_top_3_count
            player_id_object.monthly_top_10 = monthly_top_10_count
            player_id_object.monthly_top_100 = monthly_top_100_count
            player_id_object.monthly_driving_time_seconds = round(monthly_driving_time_count, 3)
            player_id_object.monthly_points = monthly_points_count


            playerinfo_nr += 1

            # LOGS_5
            stdout_5 = sys.stdout
            log_file_5 = open("log_file.log", "a")
            sys.stdout = log_file_5
            # LOGS_5
            print('playerinfo_nr: ', playerinfo_nr)
            # LOGS_5
            sys.stdout = stdout_5
            log_file_5.close()
            # LOGS_5
            
            player_id_object.save()

    # LOGS_6
    stdout_6 = sys.stdout
    log_file_6 = open("log_file.log", "a")
    sys.stdout = log_file_6
    # LOGS_6
    print('New PlayerInfo database completed!')
     # LOGS_6
    sys.stdout = stdout_6
    log_file_6.close()
    # LOGS_6

    # END of code for getting all unique players info to database PlayersInfo.
    # ******************************Launch this code if web scraping is already automated (web page is in production mode).












    # NOTE: Version 2. Non-Automated PlayerInfo.

    # # ******************************Launch this code if web scraping is already not automated or database is not fully uploaded.
    # # START of code for getting all unique players info to database PlayersInfo.
    # # This code gets every PlayerID from all database leaderboards and corresponding player info.
    #
    # """Deletes PlayerInfo database every time before starting to write new one."""
    # try:
    #     player_id_delete_object = PlayersInfo.objects.all()
    #     for i in player_id_delete_object:
    #         i.delete()
    #     print('Old PlayerInfo entries deleted!')
    # except:
    #     print('PlayerInfo database was already empty!')
    # """Deletes PlayerInfo database every time before starting to write new one."""
    #
    #
    #
    # # timer
    # time_control_3 = timer()
    #
    #
    # print('Starting new PlayersInfo database!')
    #
    # player_id_database_list = []
    # player_id_obj = LeaderBoard.objects.all()
    #
    # count_to_stop = 0
    #
    # playerinfo_nr = 0
    # for i in player_id_obj:
    #
    #     # # Start. Code for controlling how many values will be saved to database. For testing purposes.
    #     # count_to_stop += 1
    #     # if count_to_stop == 1000:
    #     #     break
    #     # # End. Code for controlling how many values will be saved to database. For testing purposes.
    #
    #     if i.player_id in player_id_database_list:
    #         continue
    #
    #     else:
    #         player_id_database_list.append(i.player_id)  # Equal to TotalUniqueDrivers value.
    #
    #         leaderb_obj = LeaderBoard.objects.filter(player_id__exact=i.player_id, event_info__event_category__exact='Daily')
    #
    #         daily_events_finished_count = 0
    #         daily_sum_of_finish_places = 0
    #         daily_first_places_count = 0
    #         daily_top_3_count = 0
    #         daily_top_10_count = 0
    #         daily_top_100_count = 0
    #         daily_driving_time_count = 0
    #         daily_points_count = 0
    #
    #         for k in leaderb_obj:
    #             daily_events_finished_count += 1
    #             if k.position == 1:
    #                 daily_first_places_count += 1
    #             if k.position <= 3:
    #                 daily_top_3_count += 1
    #             if k.position <= 10:
    #                 daily_top_10_count += 1
    #             if k.position <= 100:
    #                 daily_top_100_count += 1
    #
    #             daily_sum_of_finish_places += k.position
    #             daily_driving_time_count += k.time_seconds
    #             daily_points_count += k.earned_points
    #
    #
    #         leaderb_obj = LeaderBoard.objects.filter(player_id__exact=i.player_id, event_info__event_category__exact='Daily2')
    #
    #         daily2_events_finished_count = 0
    #         daily2_sum_of_finish_places = 0
    #         daily2_first_places_count = 0
    #         daily2_top_3_count = 0
    #         daily2_top_10_count = 0
    #         daily2_top_100_count = 0
    #         daily2_driving_time_count = 0
    #         daily2_points_count = 0
    #
    #         for k in leaderb_obj:
    #             daily2_events_finished_count += 1
    #             if k.position == 1:
    #                 daily2_first_places_count += 1
    #             if k.position <= 3:
    #                 daily2_top_3_count += 1
    #             if k.position <= 10:
    #                 daily2_top_10_count += 1
    #             if k.position <= 100:
    #                 daily2_top_100_count += 1
    #
    #             daily2_sum_of_finish_places += k.position
    #             daily2_driving_time_count += k.time_seconds
    #             daily2_points_count += k.earned_points
    #
    #
    #         leaderb_obj = LeaderBoard.objects.filter(player_id__exact=i.player_id, event_info__event_category__exact='Weekly')
    #
    #         weekly_events_finished_count = 0
    #         weekly_sum_of_finish_places = 0
    #         weekly_first_places_count = 0
    #         weekly_top_3_count = 0
    #         weekly_top_10_count = 0
    #         weekly_top_100_count = 0
    #         weekly_driving_time_count = 0
    #         weekly_points_count = 0
    #
    #         for k in leaderb_obj:
    #             weekly_events_finished_count += 1
    #             if k.position == 1:
    #                 weekly_first_places_count += 1
    #             if k.position <= 3:
    #                 weekly_top_3_count += 1
    #             if k.position <= 10:
    #                 weekly_top_10_count += 1
    #             if k.position <= 100:
    #                 weekly_top_100_count += 1
    #
    #             weekly_sum_of_finish_places += k.position
    #             weekly_driving_time_count += k.time_seconds
    #             weekly_points_count += k.earned_points
    #
    #
    #         leaderb_obj = LeaderBoard.objects.filter(player_id__exact=i.player_id, event_info__event_category__exact='Weekly2')
    #
    #         weekly2_events_finished_count = 0
    #         weekly2_sum_of_finish_places = 0
    #         weekly2_first_places_count = 0
    #         weekly2_top_3_count = 0
    #         weekly2_top_10_count = 0
    #         weekly2_top_100_count = 0
    #         weekly2_driving_time_count = 0
    #         weekly2_points_count = 0
    #
    #         for k in leaderb_obj:
    #             weekly2_events_finished_count += 1
    #             if k.position == 1:
    #                 weekly2_first_places_count += 1
    #             if k.position <= 3:
    #                 weekly2_top_3_count += 1
    #             if k.position <= 10:
    #                 weekly2_top_10_count += 1
    #             if k.position <= 100:
    #                 weekly2_top_100_count += 1
    #
    #             weekly2_sum_of_finish_places += k.position
    #             weekly2_driving_time_count += k.time_seconds
    #             weekly2_points_count += k.earned_points
    #
    #         leaderb_obj = LeaderBoard.objects.filter(player_id__exact=i.player_id, event_info__event_category__exact='Monthly')
    #
    #         monthly_events_finished_count = 0
    #         monthly_sum_of_finish_places = 0
    #         monthly_first_places_count = 0
    #         monthly_top_3_count = 0
    #         monthly_top_10_count = 0
    #         monthly_top_100_count = 0
    #         monthly_driving_time_count = 0
    #         monthly_points_count = 0
    #
    #         for k in leaderb_obj:
    #             monthly_events_finished_count += 1
    #             if k.position == 1:
    #                 monthly_first_places_count += 1
    #             if k.position <= 3:
    #                 monthly_top_3_count += 1
    #             if k.position <= 10:
    #                 monthly_top_10_count += 1
    #             if k.position <= 100:
    #                 monthly_top_100_count += 1
    #
    #             monthly_sum_of_finish_places += k.position
    #             monthly_driving_time_count += k.time_seconds
    #             monthly_points_count += k.earned_points
    #
    #
    #         overall_events_finished_count = daily_events_finished_count + daily2_events_finished_count + weekly_events_finished_count + weekly2_events_finished_count + monthly_events_finished_count
    #         overall_sum_of_finish_places = daily_sum_of_finish_places + daily2_sum_of_finish_places + weekly_sum_of_finish_places + weekly2_sum_of_finish_places + monthly_sum_of_finish_places
    #         overall_first_places_count = daily_first_places_count + daily2_first_places_count + weekly_first_places_count + weekly2_first_places_count + monthly_first_places_count
    #         overall_top_3_count = daily_top_3_count + daily2_top_3_count + weekly_top_3_count + weekly2_top_3_count + monthly_top_3_count
    #         overall_top_10_count = daily_top_10_count + daily2_top_10_count + weekly_top_10_count + weekly2_top_10_count + monthly_top_10_count
    #         overall_top_100_count = daily_top_100_count + daily2_top_100_count + weekly_top_100_count + weekly2_top_100_count + monthly_top_100_count
    #         overall_driving_time_count = daily_driving_time_count + daily2_driving_time_count + weekly_driving_time_count + weekly2_driving_time_count + monthly_driving_time_count
    #         overall_points_count = daily_points_count + daily2_points_count + weekly_points_count + weekly2_points_count + monthly_points_count
    #
    #
    #         # Make obj just for getting last driven event date list.
    #         leaderb_obj = LeaderBoard.objects.filter(player_id__exact=i.player_id)
    #
    #         event_info_date_list = []
    #         for k in leaderb_obj:
    #             event_info_date_list.append(k.event_info.date)
    #         # Make obj just for getting last driven event date list.
    #
    #
    #         # START Code: Find driver's name and country from last finished even.
    #         obj = LeaderBoard.objects.filter(event_info__date__exact=find_last_date(event_info_date_list), player_id__exact=i.player_id)
    #
    #         country = ''
    #         name = ''
    #         for m in obj:
    #             country = m.country_name
    #             name = m.name
    #             break
    #         # END Code: Find driver's name and country from last finished even.
    #
    #
    #
    #         if overall_events_finished_count >= 3:    # This line limits top table to drivers who have finished certain number on events. For example: at least 3
    #
    #             player_id_object = PlayersInfo()
    #
    #             player_id_object.country_from = country
    #             player_id_object.name = name
    #             player_id_object.player_id = i.player_id
    #
    #             player_id_object.overall_events_finished = overall_events_finished_count
    #             player_id_object.overall_average_finish_place = round(float(overall_sum_of_finish_places) / overall_events_finished_count, 1)
    #             player_id_object.overall_first_places = overall_first_places_count
    #             player_id_object.overall_top_3 = overall_top_3_count
    #             player_id_object.overall_top_10 = overall_top_10_count
    #             player_id_object.overall_top_100 = overall_top_100_count
    #             player_id_object.overall_driving_time_seconds = round(overall_driving_time_count, 3)
    #             player_id_object.overall_points = overall_points_count
    #             player_id_object.overall_average_points = round(float(overall_points_count) / overall_events_finished_count, 1)
    #
    #
    #             player_id_object.daily_events_finished = daily_events_finished_count
    #             if daily_events_finished_count != 0:
    #                 player_id_object.daily_average_finish_place = round(float(daily_sum_of_finish_places) / daily_events_finished_count, 1)
    #                 player_id_object.daily_average_points = round(float(daily_points_count) / daily_events_finished_count, 1)
    #             else:
    #                 player_id_object.daily_average_finish_place = 0
    #                 player_id_object.daily_average_points = 0
    #             player_id_object.daily_first_places = daily_first_places_count
    #             player_id_object.daily_top_3 = daily_top_3_count
    #             player_id_object.daily_top_10 = daily_top_10_count
    #             player_id_object.daily_top_100 = daily_top_100_count
    #             player_id_object.daily_driving_time_seconds = round(daily_driving_time_count, 3)
    #             player_id_object.daily_points = daily_points_count
    #
    #
    #             player_id_object.daily2_events_finished = daily2_events_finished_count
    #             if daily2_events_finished_count != 0:
    #                 player_id_object.daily2_average_finish_place = round(float(daily2_sum_of_finish_places) / daily2_events_finished_count, 1)
    #                 player_id_object.daily2_average_points = round(float(daily2_points_count) / daily2_events_finished_count, 1)
    #             else:
    #                 player_id_object.daily2_average_finish_place = 0
    #                 player_id_object.daily2_average_points = 0
    #             player_id_object.daily2_first_places = daily2_first_places_count
    #             player_id_object.daily2_top_3 = daily2_top_3_count
    #             player_id_object.daily2_top_10 = daily2_top_10_count
    #             player_id_object.daily2_top_100 = daily2_top_100_count
    #             player_id_object.daily2_driving_time_seconds = round(daily2_driving_time_count, 3)
    #             player_id_object.daily2_points = daily2_points_count
    #
    #
    #             player_id_object.weekly_events_finished = weekly_events_finished_count
    #             if weekly_events_finished_count != 0:
    #                 player_id_object.weekly_average_finish_place = round(float(weekly_sum_of_finish_places) / weekly_events_finished_count, 1)
    #                 player_id_object.weekly_average_points = round(float(weekly_points_count) / weekly_events_finished_count, 1)
    #             else:
    #                 player_id_object.weekly_average_finish_place = 0
    #                 player_id_object.weekly_average_points = 0
    #             player_id_object.weekly_first_places = weekly_first_places_count
    #             player_id_object.weekly_top_3 = weekly_top_3_count
    #             player_id_object.weekly_top_10 = weekly_top_10_count
    #             player_id_object.weekly_top_100 = weekly_top_100_count
    #             player_id_object.weekly_driving_time_seconds = round(weekly_driving_time_count, 3)
    #             player_id_object.weekly_points = weekly_points_count
    #
    #
    #             player_id_object.weekly2_events_finished = weekly2_events_finished_count
    #             if weekly2_events_finished_count != 0:
    #                 player_id_object.weekly2_average_finish_place = round(float(weekly2_sum_of_finish_places) / weekly2_events_finished_count, 1)
    #                 player_id_object.weekly2_average_points = round(float(weekly2_points_count) / weekly2_events_finished_count, 1)
    #             else:
    #                 player_id_object.weekly2_average_finish_place = 0
    #                 player_id_object.weekly2_average_points = 0
    #             player_id_object.weekly2_first_places = weekly2_first_places_count
    #             player_id_object.weekly2_top_3 = weekly2_top_3_count
    #             player_id_object.weekly2_top_10 = weekly2_top_10_count
    #             player_id_object.weekly2_top_100 = weekly2_top_100_count
    #             player_id_object.weekly2_driving_time_seconds = round(weekly2_driving_time_count, 3)
    #             player_id_object.weekly2_points = weekly2_points_count
    #
    #
    #             player_id_object.monthly_events_finished = monthly_events_finished_count
    #             if monthly_events_finished_count != 0:
    #                 player_id_object.monthly_average_finish_place = round(float(monthly_sum_of_finish_places) / monthly_events_finished_count, 1)
    #                 player_id_object.monthly_average_points = round(float(monthly_points_count) / monthly_events_finished_count, 1)
    #             else:
    #                 player_id_object.monthly_average_finish_place = 0
    #                 player_id_object.monthly_average_points = 0
    #             player_id_object.monthly_first_places = monthly_first_places_count
    #             player_id_object.monthly_top_3 = monthly_top_3_count
    #             player_id_object.monthly_top_10 = monthly_top_10_count
    #             player_id_object.monthly_top_100 = monthly_top_100_count
    #             player_id_object.monthly_driving_time_seconds = round(monthly_driving_time_count, 3)
    #             player_id_object.monthly_points = monthly_points_count
    #
    #
    #             playerinfo_nr += 1
    #             print(playerinfo_nr)
    #
    #             player_id_object.save()
    #
    # print('New PlayerInfo database completed!')
    # # END of code for getting all unique players info to database PlayersInfo.
    #
    # # ******************************Launch this code if web scraping is already not automated or database is not fully uploaded.



    #NOTE: !!!!!!!!!!!!!!!!!!WARNING: Remember to comment out one of the PlayerInfo database codes version!!!!!!!!!!!!!!!!!!













    # timer
    time_control_4 = timer()

    # This block of code takes very long to go through and we actually never use this TotalUniqueDrivers table anywhere. For the sake of sparing resources and time, let's just comment it out for know.
    """Code for writing TotalUniqueDrivers database entry."""
    # player_id_obj = LeaderBoard.objects.all()

    # player_id_database_list = []
    # leaderboard_progression = 0
    # for i in player_id_obj:
    #     leaderboard_progression += 1
        
    #     a = 10
    #     if (leaderboard_progression % a) == 0: # To not make log file to record leaderboard_progression every iteration this if condition will write it after every 'a' times.
    #         # LOG_leaderboard_progression
    #         stdout_leaderboard_progression = sys.stdout
    #         log_file_leaderboard_progression = open("log_file.log", "a")
    #         sys.stdout = log_file_leaderboard_progression
    #         print("leaderboard_progression = ", leaderboard_progression)
    #         sys.stdout = stdout_leaderboard_progression
    #         log_file_leaderboard_progression.close()

    #     if i.player_id in player_id_database_list:
    #         continue
    #     else:
    #         player_id_database_list.append(i.player_id)

    #         # LOG_count
    #         stdout_total_unique_drivers = sys.stdout
    #         log_file_total_unique_drivers = open("log_file.log", "a")
    #         sys.stdout = log_file_total_unique_drivers
    #         print("TotalUniqueDrivers = ", len(player_id_database_list))
    #         sys.stdout = stdout_total_unique_drivers
    #         log_file_total_unique_drivers.close()


    # total_unique_drivers_object = TotalUniqueDrivers()
    # total_unique_drivers_object.player_id_list_len = len(player_id_database_list)
    # total_unique_drivers_object.save()
    """Code for writing TotalUniqueDrivers database entry."""


    """Code for writing TotalQualifiedDrivers database entry."""
    total_top_qualified_drivers = PlayersInfo.objects.all().count()
    print("total_top_qualified_drivers = ", total_top_qualified_drivers)

    total_top_qualified_drivers_object = TotalQualifiedDrivers()
    total_top_qualified_drivers_object.qualified_drivers = total_top_qualified_drivers
    total_top_qualified_drivers_object.save()
    """Code for writing TotalQualifiedDrivers database entry."""

    # timer
    time_control_5 = timer()










    # START of code for saving NO COUNTRY results on database.
    # This code is for me to check database to see if player has been uploaded on database with unknown country.
    try:
        no_country_name_delete_object = NoCountryNameCheck.objects.all()
        for i in no_country_name_delete_object:
            i.delete()
    except:
        pass


    no_country_object = LeaderBoard.objects.filter(country_name__exact='NO COUNTRY')


    for i in no_country_object:
        no_country = str(i.event_info.event_category) + '_' + str(i.event_info.date)

        count_no_country_name_object = NoCountryNameCheck()
        count_no_country_name_object.no_country_name = no_country
        count_no_country_name_object.save()
    # END of code for saving NO COUNTRY results on database.





    site_update_status_function('Site Update - Countries')


    # timer
    time_control_6 = timer()




    # START of code for getting all countries info to database CountriesInfo.
    # This code gets every qualified driver from PlayersInfo and adds them together.

    """Delete CountriesInfo database every time before starting to write new one."""
    countriesinfo_delete_object = CountriesInfo.objects.all()
    for i in countriesinfo_delete_object:
        i.delete()

    # LOGS_7
    stdout_7 = sys.stdout
    log_file_7 = open("log_file.log", "a")
    sys.stdout = log_file_7
    # LOGS_7
    print('Old CountriesInfo entries deleted!')
    """Delete CountriesInfo database every time before starting to write new one."""


    print('Starting new CountriesInfo database!')
    # LOGS_7
    sys.stdout = stdout_7
    log_file_7.close()
    # LOGS_7

    players_info_obj = PlayersInfo.objects.all()

    country_list = []
    for i in players_info_obj:
        if i.country_from in country_list:
            continue
        else:
            country_list.append(i.country_from)

    for i in country_list:
        players_info_country_obj = PlayersInfo.objects.filter(country_from__exact=i)

        overall_number_of_drivers = 0
        overall_events_finished = 0
        overall_average_finish_place = 0
        overall_first_places = 0
        overall_top_3 = 0
        overall_top_10 = 0
        overall_top_100 = 0
        overall_driving_time_seconds = 0
        overall_points = 0
        overall_average_points = 0

        daily_number_of_drivers = 0
        daily_events_finished = 0
        daily_average_finish_place = 0
        daily_first_places = 0
        daily_top_3 = 0
        daily_top_10 = 0
        daily_top_100 = 0
        daily_driving_time_seconds = 0
        daily_points = 0
        daily_average_points = 0

        daily2_number_of_drivers = 0
        daily2_events_finished = 0
        daily2_average_finish_place = 0
        daily2_first_places = 0
        daily2_top_3 = 0
        daily2_top_10 = 0
        daily2_top_100 = 0
        daily2_driving_time_seconds = 0
        daily2_points = 0
        daily2_average_points = 0

        weekly_number_of_drivers = 0
        weekly_events_finished = 0
        weekly_average_finish_place = 0
        weekly_first_places = 0
        weekly_top_3 = 0
        weekly_top_10 = 0
        weekly_top_100 = 0
        weekly_driving_time_seconds = 0
        weekly_points = 0
        weekly_average_points = 0

        weekly2_number_of_drivers = 0
        weekly2_events_finished = 0
        weekly2_average_finish_place = 0
        weekly2_first_places = 0
        weekly2_top_3 = 0
        weekly2_top_10 = 0
        weekly2_top_100 = 0
        weekly2_driving_time_seconds = 0
        weekly2_points = 0
        weekly2_average_points = 0

        monthly_number_of_drivers = 0
        monthly_events_finished = 0
        monthly_average_finish_place = 0
        monthly_first_places = 0
        monthly_top_3 = 0
        monthly_top_10 = 0
        monthly_top_100 = 0
        monthly_driving_time_seconds = 0
        monthly_points = 0
        monthly_average_points = 0


        for j in players_info_country_obj:

            overall_number_of_drivers += 1
            overall_events_finished += j.overall_events_finished
            overall_average_finish_place += j.overall_average_finish_place
            overall_first_places += j.overall_first_places
            overall_top_3 += j.overall_top_3
            overall_top_10 += j.overall_top_10
            overall_top_100 += j.overall_top_100
            overall_driving_time_seconds += j.overall_driving_time_seconds
            overall_points += j.overall_points

            if j.daily_events_finished != 0:
                daily_number_of_drivers += 1
            daily_events_finished += j.daily_events_finished
            daily_average_finish_place += j.daily_average_finish_place
            daily_first_places += j.daily_first_places
            daily_top_3 += j.daily_top_3
            daily_top_10 += j.daily_top_10
            daily_top_100 += j.daily_top_100
            daily_driving_time_seconds += j.daily_driving_time_seconds
            daily_points += j.daily_points

            if j.daily2_events_finished != 0:
                daily2_number_of_drivers += 1
            daily2_events_finished += j.daily2_events_finished
            daily2_average_finish_place += j.daily2_average_finish_place
            daily2_first_places += j.daily2_first_places
            daily2_top_3 += j.daily2_top_3
            daily2_top_10 += j.daily2_top_10
            daily2_top_100 += j.daily2_top_100
            daily2_driving_time_seconds += j.daily2_driving_time_seconds
            daily2_points += j.daily2_points

            if j.weekly_events_finished != 0:
                weekly_number_of_drivers += 1
            weekly_events_finished += j.weekly_events_finished
            weekly_average_finish_place += j.weekly_average_finish_place
            weekly_first_places += j.weekly_first_places
            weekly_top_3 += j.weekly_top_3
            weekly_top_10 += j.weekly_top_10
            weekly_top_100 += j.weekly_top_100
            weekly_driving_time_seconds += j.weekly_driving_time_seconds
            weekly_points += j.weekly_points

            if j.weekly2_events_finished != 0:
                weekly2_number_of_drivers += 1
            weekly2_events_finished += j.weekly2_events_finished
            weekly2_average_finish_place += j.weekly2_average_finish_place
            weekly2_first_places += j.weekly2_first_places
            weekly2_top_3 += j.weekly2_top_3
            weekly2_top_10 += j.weekly2_top_10
            weekly2_top_100 += j.weekly2_top_100
            weekly2_driving_time_seconds += j.weekly2_driving_time_seconds
            weekly2_points += j.weekly2_points


            if j.monthly_events_finished != 0:
                monthly_number_of_drivers += 1
            monthly_events_finished += j.monthly_events_finished
            monthly_average_finish_place += j.monthly_average_finish_place
            monthly_first_places += j.monthly_first_places
            monthly_top_3 += j.monthly_top_3
            monthly_top_10 += j.monthly_top_10
            monthly_top_100 += j.monthly_top_100
            monthly_driving_time_seconds += j.monthly_driving_time_seconds
            monthly_points += j.monthly_points


            overall_average_points = round(float(overall_points / overall_number_of_drivers), 1)

        if daily_number_of_drivers != 0:
            daily_average_points = round(float(daily_points / daily_number_of_drivers), 1)

        if daily2_number_of_drivers != 0:
            daily2_average_points = round(float(daily2_points / daily2_number_of_drivers), 1)

        if weekly_number_of_drivers != 0:
            weekly_average_points = round(float(weekly_points / weekly_number_of_drivers), 1)

        if weekly2_number_of_drivers != 0:
            weekly2_average_points = round(float(weekly2_points / weekly2_number_of_drivers), 1)

        if monthly_number_of_drivers != 0:
            monthly_average_points = round(float(monthly_points / monthly_number_of_drivers), 1)


        countriesinfo_object = CountriesInfo()

        countriesinfo_object.country_name = i


        countriesinfo_object.overall_number_of_drivers = overall_number_of_drivers
        countriesinfo_object.overall_events_finished = overall_events_finished
        if overall_number_of_drivers != 0:
            countriesinfo_object.overall_average_finish_place = round(float(overall_average_finish_place / overall_number_of_drivers), 1)
        else:
            countriesinfo_object.overall_average_finish_place = 0
        countriesinfo_object.overall_first_places = overall_first_places
        countriesinfo_object.overall_top_3 = overall_top_3
        countriesinfo_object.overall_top_10 = overall_top_10
        countriesinfo_object.overall_top_100 = overall_top_100
        countriesinfo_object.overall_driving_time_seconds = overall_driving_time_seconds
        countriesinfo_object.overall_points = overall_points
        countriesinfo_object.overall_average_points = overall_average_points


        countriesinfo_object.daily_number_of_drivers = daily_number_of_drivers
        countriesinfo_object.daily_events_finished = daily_events_finished
        if daily_number_of_drivers != 0:
            countriesinfo_object.daily_average_finish_place = round(float(daily_average_finish_place / daily_number_of_drivers), 1)
        else:
            countriesinfo_object.daily_average_finish_place = 0
        countriesinfo_object.daily_first_places = daily_first_places
        countriesinfo_object.daily_top_3 = daily_top_3
        countriesinfo_object.daily_top_10 = daily_top_10
        countriesinfo_object.daily_top_100 = daily_top_100
        countriesinfo_object.daily_driving_time_seconds = daily_driving_time_seconds
        countriesinfo_object.daily_points = daily_points
        countriesinfo_object.daily_average_points = daily_average_points


        countriesinfo_object.daily2_number_of_drivers = daily2_number_of_drivers
        countriesinfo_object.daily2_events_finished = daily2_events_finished
        if daily2_number_of_drivers != 0:
            countriesinfo_object.daily2_average_finish_place = round(float(daily2_average_finish_place / daily2_number_of_drivers), 1)
        else:
            countriesinfo_object.daily2_average_finish_place = 0
        countriesinfo_object.daily2_first_places = daily2_first_places
        countriesinfo_object.daily2_top_3 = daily2_top_3
        countriesinfo_object.daily2_top_10 = daily2_top_10
        countriesinfo_object.daily2_top_100 = daily2_top_100
        countriesinfo_object.daily2_driving_time_seconds = daily2_driving_time_seconds
        countriesinfo_object.daily2_points = daily2_points
        countriesinfo_object.daily2_average_points = daily2_average_points


        countriesinfo_object.weekly_number_of_drivers = weekly_number_of_drivers
        countriesinfo_object.weekly_events_finished = weekly_events_finished
        if weekly_number_of_drivers != 0:
            countriesinfo_object.weekly_average_finish_place = round(float(weekly_average_finish_place / weekly_number_of_drivers), 1)
        else:
            countriesinfo_object.weekly_average_finish_place = 0
        countriesinfo_object.weekly_first_places = weekly_first_places
        countriesinfo_object.weekly_top_3 = weekly_top_3
        countriesinfo_object.weekly_top_10 = weekly_top_10
        countriesinfo_object.weekly_top_100 = weekly_top_100
        countriesinfo_object.weekly_driving_time_seconds = weekly_driving_time_seconds
        countriesinfo_object.weekly_points = weekly_points
        countriesinfo_object.weekly_average_points = weekly_average_points


        countriesinfo_object.weekly2_number_of_drivers = weekly2_number_of_drivers
        countriesinfo_object.weekly2_events_finished = weekly2_events_finished
        if weekly2_number_of_drivers != 0:
            countriesinfo_object.weekly2_average_finish_place = round(float(weekly2_average_finish_place / weekly2_number_of_drivers), 1)
        else:
            countriesinfo_object.weekly2_average_finish_place = 0
        countriesinfo_object.weekly2_first_places = weekly2_first_places
        countriesinfo_object.weekly2_top_3 = weekly2_top_3
        countriesinfo_object.weekly2_top_10 = weekly2_top_10
        countriesinfo_object.weekly2_top_100 = weekly2_top_100
        countriesinfo_object.weekly2_driving_time_seconds = weekly2_driving_time_seconds
        countriesinfo_object.weekly2_points = weekly2_points
        countriesinfo_object.weekly2_average_points = weekly2_average_points

        countriesinfo_object.monthly_number_of_drivers = monthly_number_of_drivers
        countriesinfo_object.monthly_events_finished = monthly_events_finished
        if monthly_number_of_drivers != 0:
            countriesinfo_object.monthly_average_finish_place = round(
                float(monthly_average_finish_place / monthly_number_of_drivers), 1)
        else:
            countriesinfo_object.monthly_average_finish_place = 0
        countriesinfo_object.monthly_first_places = monthly_first_places
        countriesinfo_object.monthly_top_3 = monthly_top_3
        countriesinfo_object.monthly_top_10 = monthly_top_10
        countriesinfo_object.monthly_top_100 = monthly_top_100
        countriesinfo_object.monthly_driving_time_seconds = monthly_driving_time_seconds
        countriesinfo_object.monthly_points = monthly_points
        countriesinfo_object.monthly_average_points = monthly_average_points


        # countriesinfo_object.total_driving_time_seconds = round(total_driving_time_count, 3)

        countriesinfo_object.save()
    # END of code for getting all countries info to database CountriesInfo.






    site_update_status_function('Site Update - Driver Ranks')


    # timer
    time_control_7 = timer()






    """ !!!Note to self!!! This next commented out code section is responsible for calculating global driver and country ranks. 
    As the databese grows and driver count increases, this could take too much of a time for the server. Disable for now till the calculation are made more efficient. """
    # # NOTE: START of Code for driver world and country ranks.

    # event_category_list = ['overall', 'daily', 'daily2', 'weekly', 'weekly2', 'monthly']
    # order_variable_list = ['events_finished', 'points', 'average_points', 'average_finish_place', 'first_places',
    #                        'top_3', 'top_10', 'top_100', 'driving_time_seconds']

    # for event_category in event_category_list:
    #     for order_variable in order_variable_list:

    #         print(event_category, order_variable)

    #         def rank_function(world_rank, rank_type):
    #             count = 0
    #             for rank in world_rank:
    #                 count += 1

    #                 if rank_type == 'world':
    #                     if event_category == 'overall':
    #                         if order_variable == 'events_finished':
    #                             rank.overall_world_rank_events_finished = count
    #                             rank.save()

    #                         elif order_variable == 'points':
    #                             rank.overall_world_rank_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_points':
    #                             rank.overall_world_rank_average_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_finish_place':
    #                             rank.overall_world_rank_average_finish_place = count
    #                             rank.save()

    #                         elif order_variable == 'first_places':
    #                             rank.overall_world_rank_first_places = count
    #                             rank.save()

    #                         elif order_variable == 'top_3':
    #                             rank.overall_world_rank_top_3 = count
    #                             rank.save()

    #                         elif order_variable == 'top_10':
    #                             rank.overall_world_rank_top_10 = count
    #                             rank.save()

    #                         elif order_variable == 'top_100':
    #                             rank.overall_world_rank_top_100 = count
    #                             rank.save()

    #                         elif order_variable == 'driving_time_seconds':
    #                             rank.overall_world_rank_driving_time_seconds = count
    #                             rank.save()


    #                     elif event_category == 'daily':
    #                         if order_variable == 'events_finished':
    #                             rank.daily_world_rank_events_finished = count
    #                             rank.save()

    #                         elif order_variable == 'points':
    #                             rank.daily_world_rank_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_points':
    #                             rank.daily_world_rank_average_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_finish_place':
    #                             rank.daily_world_rank_average_finish_place = count
    #                             rank.save()

    #                         elif order_variable == 'first_places':
    #                             rank.daily_world_rank_first_places = count
    #                             rank.save()

    #                         elif order_variable == 'top_3':
    #                             rank.daily_world_rank_top_3 = count
    #                             rank.save()

    #                         elif order_variable == 'top_10':
    #                             rank.daily_world_rank_top_10 = count
    #                             rank.save()

    #                         elif order_variable == 'top_100':
    #                             rank.daily_world_rank_top_100 = count
    #                             rank.save()

    #                         elif order_variable == 'driving_time_seconds':
    #                             rank.daily_world_rank_driving_time_seconds = count
    #                             rank.save()


    #                     elif event_category == 'daily2':
    #                         if order_variable == 'events_finished':
    #                             rank.daily2_world_rank_events_finished = count
    #                             rank.save()

    #                         elif order_variable == 'points':
    #                             rank.daily2_world_rank_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_points':
    #                             rank.daily2_world_rank_average_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_finish_place':
    #                             rank.daily2_world_rank_average_finish_place = count
    #                             rank.save()

    #                         elif order_variable == 'first_places':
    #                             rank.daily2_world_rank_first_places = count
    #                             rank.save()

    #                         elif order_variable == 'top_3':
    #                             rank.daily2_world_rank_top_3 = count
    #                             rank.save()

    #                         elif order_variable == 'top_10':
    #                             rank.daily2_world_rank_top_10 = count
    #                             rank.save()

    #                         elif order_variable == 'top_100':
    #                             rank.daily2_world_rank_top_100 = count
    #                             rank.save()

    #                         elif order_variable == 'driving_time_seconds':
    #                             rank.daily2_world_rank_driving_time_seconds = count
    #                             rank.save()


    #                     elif event_category == 'weekly':
    #                         if order_variable == 'events_finished':
    #                             rank.weekly_world_rank_events_finished = count
    #                             rank.save()

    #                         elif order_variable == 'points':
    #                             rank.weekly_world_rank_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_points':
    #                             rank.weekly_world_rank_average_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_finish_place':
    #                             rank.weekly_world_rank_average_finish_place = count
    #                             rank.save()

    #                         elif order_variable == 'first_places':
    #                             rank.weekly_world_rank_first_places = count
    #                             rank.save()

    #                         elif order_variable == 'top_3':
    #                             rank.weekly_world_rank_top_3 = count
    #                             rank.save()

    #                         elif order_variable == 'top_10':
    #                             rank.weekly_world_rank_top_10 = count
    #                             rank.save()

    #                         elif order_variable == 'top_100':
    #                             rank.weekly_world_rank_top_100 = count
    #                             rank.save()

    #                         elif order_variable == 'driving_time_seconds':
    #                             rank.weekly_world_rank_driving_time_seconds = count
    #                             rank.save()


    #                     elif event_category == 'weekly2':
    #                         if order_variable == 'events_finished':
    #                             rank.weekly2_world_rank_events_finished = count
    #                             rank.save()

    #                         elif order_variable == 'points':
    #                             rank.weekly2_world_rank_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_points':
    #                             rank.weekly2_world_rank_average_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_finish_place':
    #                             rank.weekly2_world_rank_average_finish_place = count
    #                             rank.save()

    #                         elif order_variable == 'first_places':
    #                             rank.weekly2_world_rank_first_places = count
    #                             rank.save()

    #                         elif order_variable == 'top_3':
    #                             rank.weekly2_world_rank_top_3 = count
    #                             rank.save()

    #                         elif order_variable == 'top_10':
    #                             rank.weekly2_world_rank_top_10 = count
    #                             rank.save()

    #                         elif order_variable == 'top_100':
    #                             rank.weekly2_world_rank_top_100 = count
    #                             rank.save()

    #                         elif order_variable == 'driving_time_seconds':
    #                             rank.weekly2_world_rank_driving_time_seconds = count
    #                             rank.save()


    #                     elif event_category == 'monthly':
    #                         if order_variable == 'events_finished':
    #                             rank.monthly_world_rank_events_finished = count
    #                             rank.save()

    #                         elif order_variable == 'points':
    #                             rank.monthly_world_rank_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_points':
    #                             rank.monthly_world_rank_average_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_finish_place':
    #                             rank.monthly_world_rank_average_finish_place = count
    #                             rank.save()

    #                         elif order_variable == 'first_places':
    #                             rank.monthly_world_rank_first_places = count
    #                             rank.save()

    #                         elif order_variable == 'top_3':
    #                             rank.monthly_world_rank_top_3 = count
    #                             rank.save()

    #                         elif order_variable == 'top_10':
    #                             rank.monthly_world_rank_top_10 = count
    #                             rank.save()

    #                         elif order_variable == 'top_100':
    #                             rank.monthly_world_rank_top_100 = count
    #                             rank.save()

    #                         elif order_variable == 'driving_time_seconds':
    #                             rank.monthly_world_rank_driving_time_seconds = count
    #                             rank.save()

    #                 elif rank_type == 'country':
    #                     if event_category == 'overall':
    #                         if order_variable == 'events_finished':
    #                             rank.overall_country_rank_events_finished = count
    #                             rank.save()

    #                         elif order_variable == 'points':
    #                             rank.overall_country_rank_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_points':
    #                             rank.overall_country_rank_average_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_finish_place':
    #                             rank.overall_country_rank_average_finish_place = count
    #                             rank.save()

    #                         elif order_variable == 'first_places':
    #                             rank.overall_country_rank_first_places = count
    #                             rank.save()

    #                         elif order_variable == 'top_3':
    #                             rank.overall_country_rank_top_3 = count
    #                             rank.save()

    #                         elif order_variable == 'top_10':
    #                             rank.overall_country_rank_top_10 = count
    #                             rank.save()

    #                         elif order_variable == 'top_100':
    #                             rank.overall_country_rank_top_100 = count
    #                             rank.save()

    #                         elif order_variable == 'driving_time_seconds':
    #                             rank.overall_country_rank_driving_time_seconds = count
    #                             rank.save()


    #                     elif event_category == 'daily':
    #                         if order_variable == 'events_finished':
    #                             rank.daily_country_rank_events_finished = count
    #                             rank.save()

    #                         elif order_variable == 'points':
    #                             rank.daily_country_rank_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_points':
    #                             rank.daily_country_rank_average_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_finish_place':
    #                             rank.daily_country_rank_average_finish_place = count
    #                             rank.save()

    #                         elif order_variable == 'first_places':
    #                             rank.daily_country_rank_first_places = count
    #                             rank.save()

    #                         elif order_variable == 'top_3':
    #                             rank.daily_country_rank_top_3 = count
    #                             rank.save()

    #                         elif order_variable == 'top_10':
    #                             rank.daily_country_rank_top_10 = count
    #                             rank.save()

    #                         elif order_variable == 'top_100':
    #                             rank.daily_country_rank_top_100 = count
    #                             rank.save()

    #                         elif order_variable == 'driving_time_seconds':
    #                             rank.daily_country_rank_driving_time_seconds = count
    #                             rank.save()


    #                     elif event_category == 'daily2':
    #                         if order_variable == 'events_finished':
    #                             rank.daily2_country_rank_events_finished = count
    #                             rank.save()

    #                         elif order_variable == 'points':
    #                             rank.daily2_country_rank_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_points':
    #                             rank.daily2_country_rank_average_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_finish_place':
    #                             rank.daily2_country_rank_average_finish_place = count
    #                             rank.save()

    #                         elif order_variable == 'first_places':
    #                             rank.daily2_country_rank_first_places = count
    #                             rank.save()

    #                         elif order_variable == 'top_3':
    #                             rank.daily2_country_rank_top_3 = count
    #                             rank.save()

    #                         elif order_variable == 'top_10':
    #                             rank.daily2_country_rank_top_10 = count
    #                             rank.save()

    #                         elif order_variable == 'top_100':
    #                             rank.daily2_country_rank_top_100 = count
    #                             rank.save()

    #                         elif order_variable == 'driving_time_seconds':
    #                             rank.daily2_country_rank_driving_time_seconds = count
    #                             rank.save()


    #                     elif event_category == 'weekly':
    #                         if order_variable == 'events_finished':
    #                             rank.weekly_country_rank_events_finished = count
    #                             rank.save()

    #                         elif order_variable == 'points':
    #                             rank.weekly_country_rank_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_points':
    #                             rank.weekly_country_rank_average_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_finish_place':
    #                             rank.weekly_country_rank_average_finish_place = count
    #                             rank.save()

    #                         elif order_variable == 'first_places':
    #                             rank.weekly_country_rank_first_places = count
    #                             rank.save()

    #                         elif order_variable == 'top_3':
    #                             rank.weekly_country_rank_top_3 = count
    #                             rank.save()

    #                         elif order_variable == 'top_10':
    #                             rank.weekly_country_rank_top_10 = count
    #                             rank.save()

    #                         elif order_variable == 'top_100':
    #                             rank.weekly_country_rank_top_100 = count
    #                             rank.save()

    #                         elif order_variable == 'driving_time_seconds':
    #                             rank.weekly_country_rank_driving_time_seconds = count
    #                             rank.save()


    #                     elif event_category == 'weekly2':
    #                         if order_variable == 'events_finished':
    #                             rank.weekly2_country_rank_events_finished = count
    #                             rank.save()

    #                         elif order_variable == 'points':
    #                             rank.weekly2_country_rank_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_points':
    #                             rank.weekly2_country_rank_average_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_finish_place':
    #                             rank.weekly2_country_rank_average_finish_place = count
    #                             rank.save()

    #                         elif order_variable == 'first_places':
    #                             rank.weekly2_country_rank_first_places = count
    #                             rank.save()

    #                         elif order_variable == 'top_3':
    #                             rank.weekly2_country_rank_top_3 = count
    #                             rank.save()

    #                         elif order_variable == 'top_10':
    #                             rank.weekly2_country_rank_top_10 = count
    #                             rank.save()

    #                         elif order_variable == 'top_100':
    #                             rank.weekly2_country_rank_top_100 = count
    #                             rank.save()

    #                         elif order_variable == 'driving_time_seconds':
    #                             rank.weekly2_country_rank_driving_time_seconds = count
    #                             rank.save()


    #                     elif event_category == 'monthly':
    #                         if order_variable == 'events_finished':
    #                             rank.monthly_country_rank_events_finished = count
    #                             rank.save()

    #                         elif order_variable == 'points':
    #                             rank.monthly_country_rank_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_points':
    #                             rank.monthly_country_rank_average_points = count
    #                             rank.save()

    #                         elif order_variable == 'average_finish_place':
    #                             rank.monthly_country_rank_average_finish_place = count
    #                             rank.save()

    #                         elif order_variable == 'first_places':
    #                             rank.monthly_country_rank_first_places = count
    #                             rank.save()

    #                         elif order_variable == 'top_3':
    #                             rank.monthly_country_rank_top_3 = count
    #                             rank.save()

    #                         elif order_variable == 'top_10':
    #                             rank.monthly_country_rank_top_10 = count
    #                             rank.save()

    #                         elif order_variable == 'top_100':
    #                             rank.monthly_country_rank_top_100 = count
    #                             rank.save()

    #                         elif order_variable == 'driving_time_seconds':
    #                             rank.monthly_country_rank_driving_time_seconds = count
    #                             rank.save()



    #         kwargs = {
    #             '{0}_{1}'.format(event_category, 'events_finished'): 0,
    #         }

    #         if order_variable == 'events_finished':
    #             world_rank_events_finished_object = PlayersInfo.objects.filter(~Q(**kwargs)).order_by(
    #                 '-' + event_category + '_' + order_variable,
    #                 event_category + '_average_finish_place')

    #             rank_function(world_rank_events_finished_object, 'world')


    #         elif order_variable == 'points':
    #             world_rank_points = PlayersInfo.objects.filter(~Q(**kwargs)).order_by(
    #                 '-' + event_category + '_' + order_variable,
    #                 event_category + '_average_finish_place')

    #             rank_function(world_rank_points, 'world')

    #         elif order_variable == 'average_points':
    #             world_rank_average_points = PlayersInfo.objects.filter(~Q(**kwargs)).order_by(
    #                 '-' + event_category + '_' + order_variable,
    #                 event_category + '_points')

    #             rank_function(world_rank_average_points, 'world')

    #         elif order_variable == 'average_finish_place':
    #             world_rank_average_finish_place = PlayersInfo.objects.filter(~Q(**kwargs)).order_by(
    #                 event_category + '_' + order_variable,
    #                 event_category + '_points')

    #             rank_function(world_rank_average_finish_place, 'world')

    #         elif order_variable == 'first_places':
    #             world_rank_first_places = PlayersInfo.objects.filter(~Q(**kwargs)).order_by(
    #                 '-' + event_category + '_' + order_variable,
    #                 '-' + event_category + '_top_3',
    #                 '-' + event_category + '_top_10',
    #                 '-' + event_category + '_top_100',
    #                 event_category + '_average_finish_place')

    #             rank_function(world_rank_first_places, 'world')

    #         elif order_variable == 'top_3':
    #             world_rank_top_3 = PlayersInfo.objects.filter(~Q(**kwargs)).order_by(
    #                 '-' + event_category + '_' + order_variable,
    #                 '-' + event_category + '_first_places',
    #                 '-' + event_category + '_top_10',
    #                 '-' + event_category + '_top_100',
    #                 event_category + '_average_finish_place')

    #             rank_function(world_rank_top_3, 'world')

    #         elif order_variable == 'top_10':
    #             world_rank_top_10 = PlayersInfo.objects.filter(~Q(**kwargs)).order_by(
    #                 '-' + event_category + '_' + order_variable,
    #                 '-' + event_category + '_first_places',
    #                 '-' + event_category + '_top_3',
    #                 '-' + event_category + '_top_100',
    #                 event_category + '_average_finish_place')

    #             rank_function(world_rank_top_10, 'world')

    #         elif order_variable == 'top_100':
    #             world_rank_top_100 = PlayersInfo.objects.filter(~Q(**kwargs)).order_by(
    #                 '-' + event_category + '_' + order_variable,
    #                 '-' + event_category + '_first_places',
    #                 '-' + event_category + '_top_3',
    #                 '-' + event_category + '_top_10',
    #                 event_category + '_average_finish_place')

    #             rank_function(world_rank_top_100, 'world')

    #         elif order_variable == 'driving_time_seconds':
    #             world_rank_driving_time_seconds = PlayersInfo.objects.filter(~Q(**kwargs)).order_by(
    #                 '-' + event_category + '_' + order_variable,
    #                 event_category + '_average_finish_place')

    #             rank_function(world_rank_driving_time_seconds, 'world')



    #         for country in country_list:

    #             if order_variable == 'events_finished':
    #                 country_rank_events_finished_object = PlayersInfo.objects.filter(country_from__exact=country).filter(~Q(**kwargs)).order_by(
    #                     '-' + event_category + '_' + order_variable,
    #                     event_category + '_average_finish_place')

    #                 rank_function(country_rank_events_finished_object, 'country')

    #             elif order_variable == 'points':
    #                 country_rank_points = PlayersInfo.objects.filter(country_from__exact=country).filter(~Q(**kwargs)).order_by(
    #                     '-' + event_category + '_' + order_variable,
    #                     event_category + '_average_finish_place')

    #                 rank_function(country_rank_points, 'country')

    #             elif order_variable == 'average_points':
    #                 country_rank_average_points = PlayersInfo.objects.filter(country_from__exact=country).filter(~Q(**kwargs)).order_by(
    #                     '-' + event_category + '_' + order_variable,
    #                     event_category + '_points')

    #                 rank_function(country_rank_average_points, 'country')

    #             elif order_variable == 'average_finish_place':
    #                 country_rank_average_finish_place = PlayersInfo.objects.filter(country_from__exact=country).filter(~Q(**kwargs)).order_by(
    #                     event_category + '_' + order_variable,
    #                     event_category + '_points')

    #                 rank_function(country_rank_average_finish_place, 'country')

    #             elif order_variable == 'first_places':
    #                 country_rank_first_places = PlayersInfo.objects.filter(country_from__exact=country).filter(~Q(**kwargs)).order_by(
    #                     '-' + event_category + '_' + order_variable,
    #                     '-' + event_category + '_top_3',
    #                     '-' + event_category + '_top_10',
    #                     '-' + event_category + '_top_100',
    #                     event_category + '_average_finish_place')

    #                 rank_function(country_rank_first_places, 'country')

    #             elif order_variable == 'top_3':
    #                 country_rank_top_3 = PlayersInfo.objects.filter(country_from__exact=country).filter(~Q(**kwargs)).order_by(
    #                     '-' + event_category + '_' + order_variable,
    #                     '-' + event_category + '_first_places',
    #                     '-' + event_category + '_top_10',
    #                     '-' + event_category + '_top_100',
    #                     event_category + '_average_finish_place')

    #                 rank_function(country_rank_top_3, 'country')

    #             elif order_variable == 'top_10':
    #                 country_rank_top_10 = PlayersInfo.objects.filter(country_from__exact=country).filter(~Q(**kwargs)).order_by(
    #                     '-' + event_category + '_' + order_variable,
    #                     '-' + event_category + '_first_places',
    #                     '-' + event_category + '_top_3',
    #                     '-' + event_category + '_top_100',
    #                     event_category + '_average_finish_place')

    #                 rank_function(country_rank_top_10, 'country')

    #             elif order_variable == 'top_100':
    #                 country_rank_top_100 = PlayersInfo.objects.filter(country_from__exact=country).filter(~Q(**kwargs)).order_by(
    #                     '-' + event_category + '_' + order_variable,
    #                     '-' + event_category + '_first_places',
    #                     '-' + event_category + '_top_3',
    #                     '-' + event_category + '_top_10',
    #                     event_category + '_average_finish_place')

    #                 rank_function(country_rank_top_100, 'country')

    #             elif order_variable == 'driving_time_seconds':
    #                 country_rank_driving_time_seconds = PlayersInfo.objects.filter(country_from__exact=country).filter(~Q(**kwargs)).order_by(
    #                     '-' + event_category + '_' + order_variable,
    #                     event_category + '_average_finish_place')

    #                 rank_function(country_rank_driving_time_seconds, 'country')

    # # NOTE: END of Code for driver world and country ranks.












    time_control_8 = timer()








    """Code for writing TotalQualifiedCountries database entry."""
    total_top_qualified_countries_object = TotalQualifiedCountries()
    total_top_qualified_countries_object.qualified_countries = len(country_list)
    total_top_qualified_countries_object.save()
    """Code for writing TotalQualifiedCountries database entry."""







    # START code for Last database update time and total days since database active.
    import datetime

    utc = datetime.datetime.utcnow()
    utc_time_string = utc.strftime("%m.%d.%Y  %H:%M")

    # LOGS_utc_time
    stdout_time = sys.stdout
    log_file_time = open("log_file.log", "a")
    sys.stdout = log_file_time
    print("utc_time_string = ", utc_time_string)
    sys.stdout = stdout_time
    log_file_time.close()
    # LOGS_utc_time

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






    # Disable Site Update status massage.
    site_update_status_obj = SiteUpdateStatus.objects.all()
    for i in site_update_status_obj:
        i.delete()





    delta_time_all = time_control_8 - time_control_1

    # LOGS_8
    stdout_8 = sys.stdout
    log_file_8 = open("log_file.log", "a")
    sys.stdout = log_file_8
    # LOGS_8
  
    print('Web Scrapping time: ', time_control_2 - time_control_1)
    print('PlayersInfo delete database time: ', time_control_3 - time_control_2)
    print('PlayersInfo new database time: ', time_control_4 - time_control_3)
    print('Total Drivers database time: ', time_control_5 - time_control_4)
    print('CountriesInfo new database time: ', time_control_7 - time_control_6)
    print('Drivers World and County ranks new database time: ', time_control_8 - time_control_7)

    print('Total script time: ', delta_time_all, '\n\n\n\n\n')

    # LOGS_8
    sys.stdout = stdout_8
    log_file_8.close()
    # LOGS_8
