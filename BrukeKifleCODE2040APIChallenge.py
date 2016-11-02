'''
Author: Bruke Kifle
Code2040 Fellows API Challenge
Due: Tuesday, November 1, 2016
Last Edited: Tuesday, November 1, 2016 (BK)
'''

import json
import requests

token = '3324b84e29961f84ebd252cb9781e837'
github = 'https://github.com/brukekifle/code2040.git'

def step1():
    json_dict = {'token': token, 'github': github}
    parsed_data = json.dumps(json_dict)
    json_obj = json.loads(parsed_data)

    req = requests.post('http://challenge.code2040.org/api/register', data = json_obj)
    
    print (req.text)

def step2():
    orig_str = requests.post('http://challenge.code2040.org/api/reverse', data = {'token': token}).text
    reverse = orig_str[::-1]

    req = requests.post('http://challenge.code2040.org/api/reverse/validate', json = {'token': token, 'string': reverse})
    print req.text

def step3():
    need_hay_req = requests.post('http://challenge.code2040.org/api/haystack', data = {'token': token})
    need_hay_dict = json.loads(need_hay_req.text)
    haystack = need_hay_dict['haystack']
    index = haystack.index(need_hay_dict['needle'])

    req = requests.post('http://challenge.code2040.org/api/haystack/validate', json = {'token': token, 'needle': index})
    print req.text

def step4():
    prefix_req = requests.post('http://challenge.code2040.org/api/prefix', data = {'token': token})
    prefix_dict = json.loads(prefix_req.text)
    prefix = prefix_dict['prefix']
    array = prefix_dict['array']
    final_array = [elm for elm in array if elm[0:len(prefix)] != prefix]
    
    req = requests.post('http://challenge.code2040.org/api/prefix/validate', json = {'token': token, 'array': final_array})
    print req.text

def step5():
    date_game_req = requests.post('http://challenge.code2040.org/api/dating', data = {'token': token})
    date_game_dict = json.loads(date_game_req.text)
    interval = date_game_dict['interval']

    #Implemented a combination of a floor function and modular arithmetic to convert interval (in secs) to days, then hours, mins, and secs
    raw_numdays = interval / (3600.0* 24.0)
    final_num_days = int(raw_numdays) 
    raw_num_hours = 24.0 * (raw_numdays - final_num_days)
    final_num_hours = int(raw_num_hours)
    raw_num_mins = 60 * (raw_num_hours - final_num_hours)
    final_num_mins = int(raw_num_mins)
    final_num_secs = 60 * (raw_num_mins - final_num_mins)

    #Given datestamp, partition into the key parts of the ISO 8601 datestamp format 
    year = date_game_dict['datestamp'].split('-')[0]
    month = date_game_dict['datestamp'].split('-')[1]
    day = date_game_dict['datestamp'].split('-')[2].split('T')[0]
    time = date_game_dict['datestamp'].split('-')[2].split('T')[1].split(':')
    hour = time[0]
    minute = time[1]
    sec = time[2].split('Z')[0]

    #Calculate final values for year, month, day, hour, min and sec
    finalsec = final_num_secs + int(sec)
    finalmin = final_num_mins + int(minute)
    finalhour = final_num_hours + int(hour)
    finaldays = final_num_days + int(day)
    finalmonth = int(month)
    finalyear = int(year)

    #Implement checks, and adjust values accordingly
    if finalsec > 59:
        finalsec = finalsec - 60
        finalmin = finalmin + 1
    if finalmin > 59:
        finalmin = finalmin - 60
        finalhour = finalhour + 1
    if finalhour > 23:
        finaldays = finaldays + 1
        finalhour = finalhour - 24
    if month[1] in [1, 3, 5, 7, 8, 10, 12]:
        if finaldays > 30:
            finaldays = finaldays - 31
            finalmonth = finalmonth + 1
    if month[1] == 2:
        if finaldays > 27:
            finaldays = finaldays - 28
            finalmonth = finalmonth + 1
    if month[1] == [4, 6, 9, 11]:
        if finaldays > 29:
            finaldays = finaldays - 30
            finalmonth = finalmonth + 1
    if finalmonth > 11:
        finalmonth = finalmonth - 12
        finalyear = finalyear + 1

    #Satisfy ISO 8601 notation
    finalyear = str(finalyear)
    if finalmonth < 10:
        finalmonth = '0'+str(finalmonth)
    else:
        finalmonth = str(finalmonth)
    if finaldays < 10:
        finaldays = '0'+str(finaldays)
    else:
        finaldays = str(finaldays)
    if finalhour < 10:
        finalhour = '0'+str(finalhour)
    else:
        finalhour = str(finalhour)
    if finalmin < 10:
        finalmin = '0'+str(finalmin)
    else:
        finalmin = str(finalmin)
    if finalsec < 10:
        finalsec = '0'+str(int(finalsec))
    else:
        finalsec = str(int(finalsec))

    #Concatenate contents into one string
    final = finalyear + '-' + finalmonth+ '-' + finaldays + 'T' + finalhour + ':' + finalmin + ':' + finalsec + 'Z'
    
    req = requests.post('http://challenge.code2040.org/api/dating/validate', json = {'token': token, 'datestamp': final})

    print req.text
