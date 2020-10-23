import sys
import io
import datetime
import traceback
import urllib3

urllib3.disable_warnings()

sys.path.append('../')

import requests
from Nations_dict import nations
import URL_eventId_date_extractor as ids
from Time_String_Converter import time_converter
from timeit import default_timer as timer


before = timer()


def scrapping(start_index, end_index):

    # List of events ID's
    list_of_ids = [ids.daily_previous_1_ID, ids.daily2_previous_1_ID, ids.weekly_previous_1_ID, ids.weekly2_previous_1_ID, ids.monthly_previous_1_ID,
                   ids.daily_previous_2_ID, ids.daily2_previous_2_ID, ids.weekly_previous_2_ID, ids.weekly2_previous_2_ID, ids.monthly_previous_2_ID,
                   ids.daily_previous_3_ID, ids.daily2_previous_3_ID, ids.weekly_previous_3_ID, ids.weekly2_previous_3_ID, ids.monthly_previous_3_ID,
                   ids.daily_previous_4_ID, ids.daily2_previous_4_ID, ids.weekly_previous_4_ID, ids.weekly2_previous_4_ID, ids.monthly_previous_4_ID,
                   ids.daily_previous_5_ID, ids.daily2_previous_5_ID, ids.weekly_previous_5_ID, ids.weekly2_previous_5_ID, ids.monthly_previous_5_ID,
                   ids.daily_previous_6_ID, ids.daily2_previous_6_ID, ids.weekly_previous_6_ID, ids.weekly2_previous_6_ID, ids.monthly_previous_6_ID,
                   ids.daily_previous_7_ID, ids.daily2_previous_7_ID, ids.weekly_previous_7_ID, ids.weekly2_previous_7_ID, ids.monthly_previous_7_ID,
                   ids.daily_previous_8_ID, ids.daily2_previous_8_ID, ids.weekly_previous_8_ID, ids.weekly2_previous_8_ID, ids.monthly_previous_8_ID,
                   ids.daily_previous_9_ID, ids.daily2_previous_9_ID, ids.weekly_previous_9_ID, ids.weekly2_previous_9_ID, ids.monthly_previous_9_ID,
                   ]

    # Events dates from each event history.
    list_of_dates = [ids.daily_previous_1_date, ids.daily2_previous_1_date, ids.weekly_previous_1_date, ids.weekly2_previous_1_date, ids.monthly_previous_1_date,
                     ids.daily_previous_2_date, ids.daily2_previous_2_date, ids.weekly_previous_2_date, ids.weekly2_previous_2_date, ids.monthly_previous_2_date,
                     ids.daily_previous_3_date, ids.daily2_previous_3_date, ids.weekly_previous_3_date, ids.weekly2_previous_3_date, ids.monthly_previous_3_date,
                     ids.daily_previous_4_date, ids.daily2_previous_4_date, ids.weekly_previous_4_date, ids.weekly2_previous_4_date, ids.monthly_previous_4_date,
                     ids.daily_previous_5_date, ids.daily2_previous_5_date, ids.weekly_previous_5_date, ids.weekly2_previous_5_date, ids.monthly_previous_5_date,
                     ids.daily_previous_6_date, ids.daily2_previous_6_date, ids.weekly_previous_6_date, ids.weekly2_previous_6_date, ids.monthly_previous_6_date,
                     ids.daily_previous_7_date, ids.daily2_previous_7_date, ids.weekly_previous_7_date, ids.weekly2_previous_7_date, ids.monthly_previous_7_date,
                     ids.daily_previous_8_date, ids.daily2_previous_8_date, ids.weekly_previous_8_date, ids.weekly2_previous_8_date, ids.monthly_previous_8_date,
                     ids.daily_previous_9_date, ids.daily2_previous_9_date, ids.weekly_previous_9_date, ids.weekly2_previous_9_date, ids.monthly_previous_9_date,
                     ]

    # List with event name strings.
    list_of_event_categories = ['Daily', 'Daily2', 'Weekly', 'Weekly2', 'Monthly',
                                'Daily', 'Daily2', 'Weekly', 'Weekly2', 'Monthly',
                                'Daily', 'Daily2', 'Weekly', 'Weekly2', 'Monthly',
                                'Daily', 'Daily2', 'Weekly', 'Weekly2', 'Monthly',
                                'Daily', 'Daily2', 'Weekly', 'Weekly2', 'Monthly',
                                'Daily', 'Daily2', 'Weekly', 'Weekly2', 'Monthly',
                                'Daily', 'Daily2', 'Weekly', 'Weekly2', 'Monthly',
                                'Daily', 'Daily2', 'Weekly', 'Weekly2', 'Monthly',
                                'Daily', 'Daily2', 'Weekly', 'Weekly2', 'Monthly',
                                ]


    # Run FOR loop to gather data from events.
    # Dirt Rally official site saves last 9 events from each category. 45 in total.

    # Change indexes for range():
    # start_index
    # end_index

    count_no_country_name = 0
    for w in range(start_index, end_index):


        # LOGS_1: Code for writing/appending all print() outputs to log file.
        # Every print() that is located between two LOGS code blocks is not printed to console.
        # To show prints in console again, LOGS code blocks should be commented out.
        stdout_1 = sys.stdout
        log_file_1 = open("log_file.log", "a")
        sys.stdout = log_file_1
        # LOGS_1: Code for writing/appending all print() outputs to log file. Everything that is between this code block and next LOGS code block will be writen/appended to log file.


        # Get this API URL from web browsers [Development Tools(F12)] - [Network] - [XHR and Fetch]
        my_url = "https://dirtgame.com/dirtrally/us/api/event?assists=any&eventId=" + list_of_ids[w] + "&group=all&leaderboard=true&nameSearch=&noCache=1532867543790&number=10&page=1&stageId=0&wheel=any"


        # Safety 'while' block to make sure response did not return zero 'LeaderboardTotal' meaning request did not work correctlly. If 'LeaderboardTotal' is zero, repeat the request for same page till 'LeaderboardTotal' has realy value.
        while_loop_times = 0
        while True:

            while_loop_times += 1
            if while_loop_times >= 100:
                break

            response = requests.get(my_url, verify=False)

            numberPages = response.json()['Pages']
            numberDrivers = response.json()['LeaderboardTotal']

            if numberPages == 0 or numberDrivers == 0:
                print("Repeat main request due to Pages = 0 OR Drivers = 0")
                continue
            else:
                break


        event_category = list_of_event_categories[w]
        date = list_of_dates[w]
        event_name = response.json()['EventName']
        event_location = response.json()['LocationName']
        stage_name = response.json()['StageName']
        time_of_day = response.json()['TimeOfDay']
        weather = response.json()['WeatherText']
        number_of_pages = response.json()['Pages']
        number_of_drivers = response.json()['LeaderboardTotal']

        print("\n\n" + event_category)
        print(date)
        print(event_name)
        print(event_location)
        print(stage_name)
        print(time_of_day)
        print(weather)
        print(number_of_pages)
        print(number_of_drivers, "\n")

        # LOGS_1: Code for writing/appending all print() outputs to log file.
        sys.stdout = stdout_1
        log_file_1.close()
        # LOGS_1: Code for writing/appending all print() outputs to log file. Everything that is behind this code block will be printed to console.



        # This for loop requests all event entries page by page.
        position = []
        country = []
        player_names = []
        vehicle = []
        finish_time = []
        diff_1st = []
        player_id = []
        for i in range(1, number_of_pages + 1):


            # LOGS_2
            stdout_2 = sys.stdout
            log_file_2 = open("log_file.log", "a")
            sys.stdout = log_file_2
            # LOGS_2

            my_url = "https://dirtgame.com/dirtrally/us/api/event?assists=any&eventId=" + list_of_ids[w] + "&group=all&leaderboard=true&nameSearch=&noCache=1&number=10&page=" + str(i) + "&stageId=0&wheel=any"


            # Safety 'while' block to make sure response did not return empty 'Entries' list. If 'Entries' is empty, repeat the request for same page till 'Entries' list contains data.
            while True:
                response = requests.get(my_url, verify=False)

                if len(response.json()['Entries']) == 0:
                    print("Repeat request due to 'Entries' list being empty")
                    continue
                else:
                    break


            # This 'if' block lets through pages: if it is not the last page for event OR if the last page ends with exactly 10 drivers (last number_of_drivers digit is 0). For example number_of_drivers is 970.
            if i != number_of_pages or [int(k) for k in str(number_of_drivers)][-1] == 0:
                for j in range(10):
                    position.append(str(response.json()['Entries'][j]['Position']))
                    country.append(nationality_numbers(response.json()['Entries'][j]['NationalityImage']))
                    if response.json()['Entries'][j]['Name'] == '':
                        player_names.append('NO NAME')
                    else:
                        player_names.append(response.json()['Entries'][j]['Name'])
                    vehicle.append(response.json()['Entries'][j]['VehicleName'])
                    finish_time.append(response.json()['Entries'][j]['Time'])
                    diff_1st.append(response.json()['Entries'][j]['DiffFirst'])
                    player_id.append(str(response.json()['Entries'][j]['PlayerId']))

                    print(str(response.json()['Entries'][j]['Position']) + '  ' + str(event_category) + '  ' + str(date) + ' ')

            # This 'else' block and for loop goes through drivers on the last page of the event. For example last 7 drivers if number_of_drivers is 927.
            else:
                for j in range([int(k) for k in str(number_of_drivers)][-1]):
                    position.append(str(response.json()['Entries'][j]['Position']))
                    country.append(nationality_numbers(response.json()['Entries'][j]['NationalityImage']))
                    if response.json()['Entries'][j]['Name'] == '':
                        player_names.append('NO NAME')
                    else:
                        player_names.append(response.json()['Entries'][j]['Name'])
                    vehicle.append(response.json()['Entries'][j]['VehicleName'])
                    finish_time.append(response.json()['Entries'][j]['Time'])
                    diff_1st.append(response.json()['Entries'][j]['DiffFirst'])
                    player_id.append(str(response.json()['Entries'][j]['PlayerId']))

                    print(str(response.json()['Entries'][j]['Position']) + '  ' + str(event_category) + '  ' + str(date) + ' ')

            # LOGS_2
            sys.stdout = stdout_2
            log_file_2.close()
            # LOGS_2



        # This for loop zips all the individual lists of values into one list.
        time_seconds = []
        for h in finish_time:
            time_seconds.append(str(time_converter(h)))

        zipped_leaderboard = list(zip(position, country, player_names, vehicle, finish_time, time_seconds, diff_1st, player_id))


        # This loop count how many drivers were registered with no country on official site.
        for i in country:
            if i == 'NO COUNTRY':
                count_no_country_name += 1


        # Creates file names and opens the files.
        f = 'file placeholder variable'
        if list_of_event_categories[w] == 'Daily':

            filename = 'Leaderboard_txt/1. Daily/' + list_of_event_categories[w] + '_' + list_of_dates[w] + '.txt'
            f = io.open(filename, 'w', encoding='utf-8')

        elif list_of_event_categories[w] == 'Daily2':

            filename = 'Leaderboard_txt/2. Daily2/' + list_of_event_categories[w] + '_' + list_of_dates[w] + '.txt'
            f = io.open(filename, 'w', encoding='utf-8')

        elif list_of_event_categories[w] == 'Weekly':

            filename = 'Leaderboard_txt/3. Weekly/' + list_of_event_categories[w] + '_' + list_of_dates[w] + '.txt'
            f = io.open(filename, 'w', encoding='utf-8')

        elif list_of_event_categories[w] == 'Weekly2':

            filename = 'Leaderboard_txt/4. Weekly2/' + list_of_event_categories[w] + '_' + list_of_dates[w] + '.txt'
            f = io.open(filename, 'w', encoding='utf-8')

        elif list_of_event_categories[w] == 'Monthly':

            filename = 'Leaderboard_txt/5. Monthly/' + list_of_event_categories[w] + '_' + list_of_dates[w] + '.txt'
            f = io.open(filename, 'w', encoding='utf-8')


        # Writes all the gathered data for particular event to file and closes it.
        f.write('Event Category: ' + str(event_category) + '\n')
        f.write('Date: ' + str(date) + '\n')
        f.write('Event Name: ' + str(event_name) + '\n')
        f.write('Location: ' + str(event_location) + '\n')
        f.write('Stage: ' + str(stage_name) + '\n')
        f.write('Time of the day: ' + str(time_of_day) + '\n')
        f.write('Weather: ' + str(weather) + '\n')
        f.write('Pages: ' + str(number_of_pages) + '\n')
        f.write('Drivers: ' + str(number_of_drivers) + '\n')

        f.write('Leaderboard: ' + str(zipped_leaderboard))

        f.close()


    # LOGS_3
    stdout_3 = sys.stdout
    log_file_3 = open("log_file.log", "a")
    sys.stdout = log_file_3
    # LOGS_3

    print('\ncount_no_country_name = ', count_no_country_name)

    after = timer()
    delta_time = after - before
    print('\n\ndelta time: ', delta_time)
    now = datetime.datetime.now()
    print("Web scraping end date and time : ")
    print(now.strftime("%Y-%m-%d %H:%M:%S"))

    print("\n\n ==================================================== END OF THE DAILY WEB SCRAPING SCRIPT ==================================================== \n\n\n\n\n")

    # LOGS_3
    sys.stdout = stdout_3
    log_file_3.close()
    # LOGS_3







# Gets integer value from string.
def nationality_numbers(string):
    space_string = string.replace('/', ' ').replace('.', ' ')
    try:
        number = int([n for n in space_string.split() if n.isdigit()][0])

        return nations(number)

    except:
        print('No country registered on official site for this driver.')
        number = 0
        return nations(number)




# Launch scraping() function through this log_Exceptions() function to print out exception in log file.
def log_Exceptions():

    try:
        scrapping(0, 5)

    except Exception:

        # LOGS_4
        stdout_4 = sys.stdout
        log_file_4 = open("log_file.log", "a")
        sys.stdout = log_file_4
        # LOGS_4

        print('------------------------------------------ scrapping Exception ------------------------------------------')
        print(traceback.format_exc())

        # LOGS_4
        sys.stdout = stdout_4
        log_file_4.close()
        # LOGS_4




# Launch this whole file through this function
log_Exceptions()
