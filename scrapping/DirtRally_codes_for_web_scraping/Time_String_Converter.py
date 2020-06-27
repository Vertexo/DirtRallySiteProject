

def time_converter(t_string):

    if len(t_string) == 9:
        t_list = [x for x in t_string]

        minutes = int(str(t_list[0] + str(t_list[1])))
        seconds = int(str(t_list[3] + str(t_list[4])))
        miliseconds = float('0.' + str(t_list[6] + str(t_list[7]) + str(t_list[8])))

        all_in_seconds = round((minutes * 60 + seconds + miliseconds), 3)

        return all_in_seconds


    elif len(t_string) == 12:
        t_list = [x for x in t_string]

        hours = int(str(t_list[0] + str(t_list[1])))
        minutes = int(str(t_list[3] + str(t_list[4])))
        seconds = int(str(t_list[6] + str(t_list[7])))
        miliseconds = float('0.' + str(t_list[9] + str(t_list[10]) + str(t_list[11])))

        all_in_seconds = round((hours * 3600 + minutes * 60 + seconds + miliseconds), 3)

        return all_in_seconds
