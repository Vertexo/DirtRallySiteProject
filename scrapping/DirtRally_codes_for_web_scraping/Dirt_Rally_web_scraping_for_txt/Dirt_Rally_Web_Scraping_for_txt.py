import sys
import codecs


sys.path.append('..')

import requests
from Nations_dict import nations
import URL_eventId_date_extractor as ids
from Time_String_Converter import time_converter
from timeit import default_timer as timer




def scrapping(start_index, end_index):

    before = timer()

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

        # Get this URL from web browsers [Development Tools(F12)] - [Network] - [XHR and Fetch]
        my_url = "https://www.dirtgame.com/us/api/event?assists=any&eventId=" + list_of_ids[w] + "&group=all&leaderboard=true&nameSearch=&noCache=1532867543790&number=10&page=1&stageId=0&wheel=any"

        response = requests.get(my_url)
        response.raise_for_status()  # raise exception if invalid response

        event_category = list_of_event_categories[w]
        date = list_of_dates[w]
        event_name = response.json()['EventName']
        event_location = response.json()['LocationName']
        stage_name = response.json()['StageName']
        time_of_day = response.json()['TimeOfDay']
        weather = response.json()['WeatherText']
        number_of_pages = response.json()['Pages']
        number_of_drivers = response.json()['LeaderboardTotal']


        print(event_category)
        print(date)
        print(event_name)
        print(event_location)
        print(stage_name)
        print(time_of_day)
        print(weather)
        print(number_of_pages)
        print(number_of_drivers)


        # Gets integer value from string.

        def nationality_numbers(string):
            space_string = string.replace('/', ' ').replace('.', ' ')
            try:
                number = int([n for n in space_string.split() if n.isdigit()][0])

                return nations(number)

            except:
                print('No country registered on official site.')
                number = 0
                return nations(number)



        position = []
        country = []
        player_names = []
        vehicle = []
        finish_time = []
        diff_1st = []
        player_id = []


        for i in range(1, number_of_pages + 1):
            my_url = "https://www.dirtgame.com/us/api/event?assists=any&eventId=" + list_of_ids[w] + "&group=all&leaderboard=true&nameSearch=&noCache=1&number=10&page=" + str(i) + "&stageId=0&wheel=any"

            response = requests.get(my_url)
            response.raise_for_status()  # raise exception if invalid response

            # print(str(response.json()['Entries']))

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


        time_seconds = []

        for h in finish_time:
            time_seconds.append(str(time_converter(h)))


        zipped_leaderboard = list(zip(position, country, player_names, vehicle, finish_time, time_seconds, diff_1st, player_id))

        # print(position)
        # print(country)
        # print(player_names)
        # print(vehicle)
        # print(finish_time)
        # print(time_seconds)
        # print(diff_1st)
        # print(player_id, '\n')
        # print(zipped_leaderboard, '\n')


        for i in country:
            if i == 'NO COUNTRY':
                count_no_country_name += 1




        if number_of_pages == 0:
            raise NameError('Scraped Entries were empty for some reason with 0 pages and 0 drivers!!!')




        if list_of_event_categories[w] == 'Daily':

            filename = 'Leaderboard_txt/1. Daily/' + list_of_event_categories[w] + '_' + list_of_dates[w] + '.txt'
            f = codecs.open(filename, 'w', 'utf-8')

        elif list_of_event_categories[w] == 'Daily2':

            filename = 'Leaderboard_txt/2. Daily2/' + list_of_event_categories[w] + '_' + list_of_dates[w] + '.txt'
            f = codecs.open(filename, 'w', 'utf-8')

        elif list_of_event_categories[w] == 'Weekly':

            filename = 'Leaderboard_txt/3. Weekly/' + list_of_event_categories[w] + '_' + list_of_dates[w] + '.txt'
            f = codecs.open(filename, 'w', 'utf-8')

        elif list_of_event_categories[w] == 'Weekly2':

            filename = 'Leaderboard_txt/4. Weekly2/' + list_of_event_categories[w] + '_' + list_of_dates[w] + '.txt'
            f = codecs.open(filename, 'w', 'utf-8')

        elif list_of_event_categories[w] == 'Monthly':

            filename = 'Leaderboard_txt/5. Monthly/' + list_of_event_categories[w] + '_' + list_of_dates[w] + '.txt'
            f = codecs.open(filename, 'w', 'utf-8')



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



    after = timer()
    delta_time = after - before
    print('delta time: ', delta_time)


    print('count_no_country_name = ', count_no_country_name)





# START. Make function repeat in case of an error.
import traceback

def repeat_if_error():
    error_count = 0
    while True:

        try:
            print('----------------------TRY-------------------------')
            scrapping(0, 5)
            break

        except Exception:
            error_count += 1
            print('------------------------------------------ ', 'Error number: ', error_count, ' ------------------------------------------')
            print(traceback.format_exc())
            continue

    print('Error_count = ', error_count)
# END. Make function repeat in case of an error.


repeat_if_error()

