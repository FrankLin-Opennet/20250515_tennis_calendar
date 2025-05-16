import requests
import pandas as pd
from itertools import product

# set vars
TEST_MODE = 0
URL_LINK = "https://api.sportdraw.com.tw/api/AdminDraw/Schedule"

PLACE_DICT = [
    {"name": "古亭河濱公園", "Id1st": 28},
    {"name": "彩虹河濱公園", "Id1st": 19},
    # more here
]

YEAR_MONTH_LIST = [
    {"year": 2025, "month": 7},
    {"year": 2025, "month": 8},
    {"year": 2025, "month": 9},
    {"year": 2025, "month": 10},
    {"year": 2025, "month": 11},
    {"year": 2025, "month": 12},
    # more here
]

MEMBER_LIST = [
    {
        "memberName": "蔡**", 
        "eventName": "OpenNetT1",
        "name1st": "古亭河濱公園",
        "onName": "Irene Tsai",
    },
    {
        "memberName": "卓**", 
        "eventName": "TennisBooking",
        "name1st": "古亭河濱公園",
        "onName": "Isabelle Cho",
    },
    {
        "memberName": "林**", 
        "eventName": "網球打起來",
        "name1st": "古亭河濱公園",
        "onName": "Frank Lin",
    },
    {
        "memberName": "詹**", 
        "eventName": "網球運動",
        "name1st": "彩虹河濱公園",
        "onName": "Jennings Chan",
    },
    # more here
]


if TEST_MODE:
    YEAR_MONTH_LIST = YEAR_MONTH_LIST[:1]

def get_schedule(
    place_id: int,
    year: int, 
    month: int,
):
    "https://api.sportdraw.com.tw/api/AdminDraw/Schedule?Id1st=28&Year=2025&Month=7"
    params = {
        "Id1st": place_id,
        "Year": year,
        "Month": month,
    }
    response = requests.get(URL_LINK, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


def get_all_schedule_list(
) -> list:
    
    # set vars
    schedule_list = []
    schedule_list_filtered = []
    iter_list = list(product(PLACE_DICT, YEAR_MONTH_LIST))

    # get schedule list
    for place_info, year_month in iter_list:
        place_name = place_info.get("name")
        place_id = place_info.get("Id1st")
        year = year_month.get("year")
        month = year_month.get("month")
        schedule = get_schedule(place_id, year, month)
        if schedule:
            schedule_list.extend(schedule)
            print(f"Schedule for {place_name} in {year}-{month}:")
        else:
            print(f"Failed to get schedule for {place_name} in {year}-{month}")

    # filter schedule list
    for schedule in schedule_list:
        for member in MEMBER_LIST:
            if (
                schedule.get("memberName") == member.get("memberName")
                and schedule.get("eventName") == member.get("eventName")
                and schedule.get("name1st") == member.get("name1st")
            ):
                schedule_list_filtered.append(schedule)
    
    return schedule_list_filtered


def trans_hour24_to_12(hour: int) -> str:
    start_time_hour = f"{(hour - 12 if hour > 12 else hour)}:00"
    start_time_ampm = "PM" if hour > 12 else "AM"
    start_time = f"{start_time_hour}:00 {start_time_ampm}"
    return start_time

def trans_schedule_list_to_google_calendar(
    schedule_list: list,
) -> pd.DataFrame:
    
    event_dict_list = []
    for i in schedule_list:

        place = i.get("name1st")
        event_name = i.get("eventName")
        member_name = i.get("memberName")
        time_list = i.get("list")
        print(f"Event: {event_name} at {place} by {member_name}")
        for t in time_list:

            # filter winner event
            if t.get("isWinner") == False:
                continue
            event_date = t.get("date")
            event_hour = t.get("hours")
            event_court = t.get("name3rd")
            onName = [m.get("onName") for m in MEMBER_LIST if m.get("memberName") == member_name and m.get("name1st") == place][0]
            print(f"Date: {event_date}, Hour: {event_hour}, Court: {event_court}, On Name: {onName}")

            # start create google calendar event
            subject = f"OpenNet Tennis | {place} {event_court} {event_hour}:00 by {onName}"
            start_date = pd.to_datetime(event_date).strftime("%m/%d/%Y")
            start_time = trans_hour24_to_12(event_hour)
            end_date = start_date
            end_time = trans_hour24_to_12(event_hour+1)

            event_dict = {
                "Subject": subject,
                "Start Date": start_date,
                "Start Time": start_time,
                "End Date": end_date,
                "End Time": end_time,
                "All Day Event": False,
                "Description": "TODO",
                "Location": place,
                "Private": False,
            }

            event_dict_list.append(event_dict)

    df = pd.DataFrame(event_dict_list)

    return df


def main():
    s_list = get_all_schedule_list()
    s_df = trans_schedule_list_to_google_calendar(s_list)
    s_df.to_csv("google_calendar_event.csv", index=False)

if __name__ == "__main__":
    main()


"""
example of google calendar event
Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private
Team Meeting,05/20/2025,10:00 AM,05/20/2025,11:00 AM,False,Monthly alignment call,Conference Room A,True
Doctor’s Appointment,06/01/2025, ,06/01/2025, ,True,Annual check-up,Clinic X,False
"""
