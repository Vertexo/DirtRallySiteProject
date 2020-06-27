import sys
import requests
import datetime
from bs4 import BeautifulSoup as soup



# Current and previous ID string functions. Gets string from the HTML with current and previous events ID's.
def events_daily(p_soup):
    daily_container = p_soup.find('div', {'class': "event daily"})

    daily_eventsid_list = []
    for i in range(10):
        daily_eventsid_list.append(eventid_converter(str(daily_container.h2.findAll('option')[i])))
    return daily_eventsid_list


def events_daily2(p_soup):
    daily2_container = p_soup.find('div', {'class': "event daily2"})

    daily2_eventsid_list = []
    for i in range(10):
        daily2_eventsid_list.append(eventid_converter(str(daily2_container.h2.findAll('option')[i])))

    return daily2_eventsid_list


def events_weekly(p_soup):
    weekly_container = p_soup.find('div', {'class': "event weekly"})

    weekly_eventsid_list = []
    for i in range(10):
        weekly_eventsid_list.append(eventid_converter(str(weekly_container.h2.findAll('option')[i])))

    return weekly_eventsid_list


def events_weekly2(p_soup):
    weekly2_container = p_soup.find('div', {'class': "event weekly2"})

    weekly2_eventsid_list = []
    for i in range(10):
        weekly2_eventsid_list.append(eventid_converter(str(weekly2_container.h2.findAll('option')[i])))

    return weekly2_eventsid_list


def events_monthly(p_soup):
    monthly_container = p_soup.find('div', {'class': "event monthly"})

    monthly_eventsid_list = []
    for i in range(10):
        monthly_eventsid_list.append(eventid_converter(str(monthly_container.h2.findAll('option')[i])))

    return monthly_eventsid_list




# Previous date string functions. Gets string from the HTML with previous events date.
def events_daily_dates(p_soup):
    daily_container = p_soup.find('div', {'class': "event daily"})

    daily_events_dates_list = []
    for i in range(1, 10):
        daily_events_dates_list.append(event_date_converter(str(daily_container.h2.findAll('option')[i])))

    return daily_events_dates_list


def events_daily2_dates(p_soup):
    daily2_container = p_soup.find('div', {'class': "event daily2"})

    daily2_events_dates_list = []
    for i in range(1, 10):
        daily2_events_dates_list.append(event_date_converter(str(daily2_container.h2.findAll('option')[i])))

    return daily2_events_dates_list


def events_weekly_dates(p_soup):
    weekly_container = p_soup.find('div', {'class': "event weekly"})

    weekly_events_dates_list = []
    for i in range(1, 10):
        weekly_events_dates_list.append(event_date_converter(str(weekly_container.h2.findAll('option')[i])))

    return weekly_events_dates_list


def events_weekly2_dates(p_soup):
    weekly2_container = p_soup.find('div', {'class': "event weekly2"})

    weekly2_events_dates_list = []
    for i in range(1, 10):
        weekly2_events_dates_list.append(event_date_converter(str(weekly2_container.h2.findAll('option')[i])))

    return weekly2_events_dates_list


def events_monthly_dates(p_soup):
    monthly_container = p_soup.find('div', {'class': "event monthly"})

    monthly_events_dates_list = []
    for i in range(1, 10):
        monthly_events_dates_list.append(event_date_converter(str(monthly_container.h2.findAll('option')[i])))

    return monthly_events_dates_list




# Two event string converter functions.
def eventid_converter(id_tag):
    eventID_list = [x for x in id_tag if x.isdigit()][:6]
    eventID_string = ''
    for s in eventID_list:
        eventID_string = eventID_string + str(s)

    return eventID_string

def event_date_converter(id_tag):
    event_date_list = [x for x in id_tag if x.isdigit() or x == '/'][6:]
    event_date_list.pop()


    if event_date_list[1] == '/' and event_date_list[3] == '/':
        event_date_list.insert(0, '0')
        event_date_list.insert(3, '0')


    elif event_date_list[2] == '/' and event_date_list[4] == '/':
        event_date_list.insert(3, '0')


    elif event_date_list[1] == '/' and event_date_list[4] == '/':
        event_date_list.insert(0, '0')



    event_date_string = ''
    for s in event_date_list:
        event_date_string = event_date_string + str(s)

    return event_date_string.replace('/', '.')




# START. Make function repeat in case of an error This part of code is not used enywhere. It is just to check 'page_soup' variable has correctly got all the HTML tags.
import traceback

def repeat_if_error_url():
    error_count_url = 0

    # LOGS
    old_stdout = sys.stdout
    log_file = open("log_file.log", "a")
    sys.stdout = log_file
    # LOGS

    print("==================================================== START OF THE DAILY WEB SCRAPING SCRIPT ==================================================== \n\n")

    now = datetime.datetime.now()
    print("Web scraping start date and time : ")
    print(now.strftime("%Y-%m-%d %H:%M:%S\n\n"))

    while True:

        # Make HTML object from URL.
        r = requests.get('https://dirtgame.com/dirtrally/us/events', verify=False)
        page_html = r.text
        page_soup_0 = soup(page_html, 'html.parser')

        try:
            print('---------------------- TRY TO GET IDs FROM URL -------------------------')
            events_daily(page_soup_0)
            break

        except Exception:
            error_count_url += 1
            print('------------------------------------------ ', 'Error number: ', error_count_url, ' ------------------------------------------')
            print(traceback.format_exc())
            continue

    print('Error_count_URL = ', error_count_url, "\n\n")

    # LOGS
    sys.stdout = old_stdout
    log_file.close()
    # LOGS

    return page_soup_0

page_soup = repeat_if_error_url()
# END. Make function repeat in case of an error This part of code is not used enywhere. It is just to check 'page_soup' variable has correctly got all the HTML tags.











# Function caller variables - all events IDs.

daily_current_ID = events_daily(page_soup)[0]
daily_previous_1_ID = events_daily(page_soup)[1]
daily_previous_2_ID = events_daily(page_soup)[2]
daily_previous_3_ID = events_daily(page_soup)[3]
daily_previous_4_ID = events_daily(page_soup)[4]
daily_previous_5_ID = events_daily(page_soup)[5]
daily_previous_6_ID = events_daily(page_soup)[6]
daily_previous_7_ID = events_daily(page_soup)[7]
daily_previous_8_ID = events_daily(page_soup)[8]
daily_previous_9_ID = events_daily(page_soup)[9]


daily2_current_ID = events_daily2(page_soup)[0]
daily2_previous_1_ID = events_daily2(page_soup)[1]
daily2_previous_2_ID = events_daily2(page_soup)[2]
daily2_previous_3_ID = events_daily2(page_soup)[3]
daily2_previous_4_ID = events_daily2(page_soup)[4]
daily2_previous_5_ID = events_daily2(page_soup)[5]
daily2_previous_6_ID = events_daily2(page_soup)[6]
daily2_previous_7_ID = events_daily2(page_soup)[7]
daily2_previous_8_ID = events_daily2(page_soup)[8]
daily2_previous_9_ID = events_daily2(page_soup)[9]


weekly_current_ID = events_weekly(page_soup)[0]
weekly_previous_1_ID = events_weekly(page_soup)[1]
weekly_previous_2_ID = events_weekly(page_soup)[2]
weekly_previous_3_ID = events_weekly(page_soup)[3]
weekly_previous_4_ID = events_weekly(page_soup)[4]
weekly_previous_5_ID = events_weekly(page_soup)[5]
weekly_previous_6_ID = events_weekly(page_soup)[6]
weekly_previous_7_ID = events_weekly(page_soup)[7]
weekly_previous_8_ID = events_weekly(page_soup)[8]
weekly_previous_9_ID = events_weekly(page_soup)[9]


weekly2_current_ID = events_weekly2(page_soup)[0]
weekly2_previous_1_ID = events_weekly2(page_soup)[1]
weekly2_previous_2_ID = events_weekly2(page_soup)[2]
weekly2_previous_3_ID = events_weekly2(page_soup)[3]
weekly2_previous_4_ID = events_weekly2(page_soup)[4]
weekly2_previous_5_ID = events_weekly2(page_soup)[5]
weekly2_previous_6_ID = events_weekly2(page_soup)[6]
weekly2_previous_7_ID = events_weekly2(page_soup)[7]
weekly2_previous_8_ID = events_weekly2(page_soup)[8]
weekly2_previous_9_ID = events_weekly2(page_soup)[9]


monthly_current_ID = events_monthly(page_soup)[0]
monthly_previous_1_ID = events_monthly(page_soup)[1]
monthly_previous_2_ID = events_monthly(page_soup)[2]
monthly_previous_3_ID = events_monthly(page_soup)[3]
monthly_previous_4_ID = events_monthly(page_soup)[4]
monthly_previous_5_ID = events_monthly(page_soup)[5]
monthly_previous_6_ID = events_monthly(page_soup)[6]
monthly_previous_7_ID = events_monthly(page_soup)[7]
monthly_previous_8_ID = events_monthly(page_soup)[8]
monthly_previous_9_ID = events_monthly(page_soup)[9]



# Function caller variables - all previous events dates.

daily_previous_1_date = events_daily_dates(page_soup)[0]
daily_previous_2_date = events_daily_dates(page_soup)[1]
daily_previous_3_date = events_daily_dates(page_soup)[2]
daily_previous_4_date = events_daily_dates(page_soup)[3]
daily_previous_5_date = events_daily_dates(page_soup)[4]
daily_previous_6_date = events_daily_dates(page_soup)[5]
daily_previous_7_date = events_daily_dates(page_soup)[6]
daily_previous_8_date = events_daily_dates(page_soup)[7]
daily_previous_9_date = events_daily_dates(page_soup)[8]


daily2_previous_1_date = events_daily2_dates(page_soup)[0]
daily2_previous_2_date = events_daily2_dates(page_soup)[1]
daily2_previous_3_date = events_daily2_dates(page_soup)[2]
daily2_previous_4_date = events_daily2_dates(page_soup)[3]
daily2_previous_5_date = events_daily2_dates(page_soup)[4]
daily2_previous_6_date = events_daily2_dates(page_soup)[5]
daily2_previous_7_date = events_daily2_dates(page_soup)[6]
daily2_previous_8_date = events_daily2_dates(page_soup)[7]
daily2_previous_9_date = events_daily2_dates(page_soup)[8]


weekly_previous_1_date = events_weekly_dates(page_soup)[0]
weekly_previous_2_date = events_weekly_dates(page_soup)[1]
weekly_previous_3_date = events_weekly_dates(page_soup)[2]
weekly_previous_4_date = events_weekly_dates(page_soup)[3]
weekly_previous_5_date = events_weekly_dates(page_soup)[4]
weekly_previous_6_date = events_weekly_dates(page_soup)[5]
weekly_previous_7_date = events_weekly_dates(page_soup)[6]
weekly_previous_8_date = events_weekly_dates(page_soup)[7]
weekly_previous_9_date = events_weekly_dates(page_soup)[8]


weekly2_previous_1_date = events_weekly2_dates(page_soup)[0]
weekly2_previous_2_date = events_weekly2_dates(page_soup)[1]
weekly2_previous_3_date = events_weekly2_dates(page_soup)[2]
weekly2_previous_4_date = events_weekly2_dates(page_soup)[3]
weekly2_previous_5_date = events_weekly2_dates(page_soup)[4]
weekly2_previous_6_date = events_weekly2_dates(page_soup)[5]
weekly2_previous_7_date = events_weekly2_dates(page_soup)[6]
weekly2_previous_8_date = events_weekly2_dates(page_soup)[7]
weekly2_previous_9_date = events_weekly2_dates(page_soup)[8]


monthly_previous_1_date = events_monthly_dates(page_soup)[0]
monthly_previous_2_date = events_monthly_dates(page_soup)[1]
monthly_previous_3_date = events_monthly_dates(page_soup)[2]
monthly_previous_4_date = events_monthly_dates(page_soup)[3]
monthly_previous_5_date = events_monthly_dates(page_soup)[4]
monthly_previous_6_date = events_monthly_dates(page_soup)[5]
monthly_previous_7_date = events_monthly_dates(page_soup)[6]
monthly_previous_8_date = events_monthly_dates(page_soup)[7]
monthly_previous_9_date = events_monthly_dates(page_soup)[8]
