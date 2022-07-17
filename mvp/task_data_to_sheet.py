import todoist, os
from datetime import *
import yaml, csv, json, pickle
from td_utilities import *
# Get activity log
# with open("todoist_helper/token","r") as td_token_file:
#     td_token=td_token_file.read()
# api = todoist.TodoistAPI(td_token)

def last_dt_from_sheet():
    SPREADSHEET_ID = '1S5icWuTWrtoa2o5j6GAgGPvFgFm5ABAtuETg_tzfGME'
    service=get_gdrive_service()
    completed_times=[cell[0] for cell in service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="CompletedRaw!A:A").execute()["values"]]
    delayed_times=[cell[0] for cell in service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="Delayed!A:A").execute()["values"]]
    times=completed_times[1:]+delayed_times[1:]
    latest_time=max(times)
    # delayed_times=service.spreadsheets().values().get(SPREADSHEET_ID, "Delayed!A:A").execute()
    return datetime.strptime(latest_time,"%Y-%m-%dT%H:%M:%SZ")
    # print(latest_time)




if __name__ == '__main__':
    completed_recently = []
    delayed_recently = []
    latest_time = last_dt_from_sheet()
    # twenty_four_hours = datetime.now()-timedelta(hours=24)
    events=get_relevant_td_activities()
    for event in events:
        if event["object_type"]!="item":
            continue
        if datetime.strptime(event["event_date"],"%Y-%m-%dT%H:%M:%SZ")<latest_time:
            continue
        if event["event_type"]=="completed":
            completed_recently.append(event)
        elif event["event_type"]=="updated" and "due_date" in event["extra_data"]:
            delayed_recently.append(event)
    SPREADSHEET_ID = '1S5icWuTWrtoa2o5j6GAgGPvFgFm5ABAtuETg_tzfGME'
    service=get_gdrive_service()
    append_events_to_sheet(completed_recently,"CompletedRaw",SPREADSHEET_ID,service=service)
    append_events_to_sheet(delayed_recently,"Delayed",SPREADSHEET_ID,service=service)
