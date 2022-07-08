from datetime import *
import todoist, pickle
import os, yaml, csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from operator import itemgetter
from todoist_api_python.api import TodoistAPI

with open("token.secret","r") as token_file:
    token=token_file.read()

api = todoist.TodoistAPI(token)
other_api = TodoistAPI(token)

def get_api():
    api.sync()
    return api

def get_relevant_td_activities():
    api.sync()
    events = api.activity.get()["events"]
    return events

def get_gdrive_service():
    creds=None
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as gdrive_token:
            creds = pickle.load(gdrive_token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gdrive-creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as gdrive_token:
            pickle.dump(creds, gdrive_token)
    service = build('sheets', 'v4', credentials=creds)
    return service

def append_events_to_sheet(event_list,target_sheet,spreadsheet_id,service=None):
    #make sure I have a service set up
    if service is None:
        service=get_gdrive_service()
    try:
        headings=sheets.values().get(
            spreadsheetId=spreadsheet_id,
            range=target_sheet+"!A1:Z1"
        ).execute().get('values',[])[0]
    except Exception as e:
        headings=[]
    sheets = service.spreadsheets()
    for event in event_list:
        headings_changed=False
        next_line=[]
        for heading in headings:
            # print("heading",heading)
            # print("event",yaml.dump(event)
            if heading in event:
                next_line.append(event[heading])
            elif heading in event["extra_data"]:
                next_line.append(event["extra_data"][heading])
            else:
                next_line.append("")
        for event_key in event:
            if event_key == "extra_data":
                continue
            if event_key not in headings:
                headings_changed=True
                headings.append(event_key)
                next_line.append(event[event_key])
        for extra_key in event["extra_data"]:
            if extra_key not in headings:
                headings_changed=True
                headings.append(extra_key)
                next_line.append(event["extra_data"][extra_key])
        # print(headings)
        if headings_changed:
            sheets.values().update(
                spreadsheetId=spreadsheet_id,
                range=target_sheet+"!A1:Z1",
                valueInputOption="USER_ENTERED",
                body={
                    'values':[headings],
                    'majorDimension':"ROWS",
                }
            ).execute().get('values',[])
        # print("next line",next_line)
        id_index=headings.index("id")+1
        id_column_letter=chr(ord('@')+id_index)
        id_column=sheets.values().get(
            spreadsheetId=spreadsheet_id,
            range=target_sheet+"!"+id_column_letter+":"+id_column_letter
        ).execute().get('values', [])
        # print("range")
        ids=[]
        for id in id_column:
            ids.append(id[0])
        # print("id_column",id_column)
        # print("IDs:")
        # exit()
        # for id in ids:
        #     print(id)
        #     print(event["id"])
        #     print(id==event["id"])
        # if str(event["id"]) in ids:
        #     print("successfully skipped a repeat")
        # print(event["id"])
        # print(type(event["id"]))
        if str(event["id"]) not in ids:
            sheets.values().append(
                spreadsheetId=spreadsheet_id,
                range=target_sheet+"!A:Z",
                valueInputOption="USER_ENTERED",
                body={
                    'values':[next_line],
                    'majorDimension':"ROWS",
                }
            ).execute()

def task_due(task):
    if task["checked"]==1:
        return False
    if task["due"] is None:
        return False
    # print(task["due"]["date"])
    date_array=task["due"]["date"].split("T")[0].split("-")
    duedate=date(int(date_array[0]),int(date_array[1]),int(date_array[2]))
    if duedate<=date.today():
        return True

def get_task_labels(task, short=True):
    output=[]
    # print(yaml.dump(task))
    for label in task["labels"]:
        label_full=api.labels.get_by_id(label)
        if short:
            if "name" in label_full:
                output.append(label_full["name"])
            else:
                print("label id",label)
                print(yaml.dump(label_full))
        else:
            output.append(label_full)
    return output

def get_due_tasks():
    tasks = []
    for task in api.state['items']:
        if task_due(task):
            tasks.append(task.data)
    return tasks

def get_projects():
    projects = []
    for project in api.state['projects']:
        projects.append(project)
    return projects

# def task_converter(task, dir=1):
#     if dir:


time_estimates={"1pom","2pom","3pom","4pom","5plus","shortbreak"}

def do_today(task,poms_booked,poms_left_today):
    #Should I set it so that p1s always are "do_today"

    # else:
    time_estimate_set=time_estimates&set(task["tag_names"])
    if time_estimate_set==set():
        do_today_bool=True
        task["tags_to_add"]="time_estimate_error"
    elif len(time_estimate_set)>1:
        do_today_bool=True
        task["tags_to_add"]="time_estimate_error"
    else:
        time_estimate_string=time_estimate_set.pop()
        if time_estimate_string=="shortbreak":
            do_today_bool=True
        elif poms_booked>=poms_left_today:
            do_today_bool=False
        else:
            poms_requested=int(time_estimate_string[0])
            if poms_requested+poms_booked<=poms_left_today:
                poms_booked+=poms_requested
                do_today_bool=True
            else:
                do_today_bool=False
        # print("Time estimate",poms_requested)
        # exit()
    return do_today_bool,poms_booked,poms_left_today
    # tasks_assessed_for_today.append(task)
def what_today(tasks_list=[],poms_booked=0,poms_left_today=4):
    if tasks_list==[]:
        print("No input task, grabbing from API")
        tasks_list=get_due_tasks()
    tasks_list=sorted(tasks_list, key=itemgetter('priority'))
    # print(yaml.dump(tasks_list))
    for task in tasks_list:
        task["tag_names"]=get_task_labels(task)
        task["do_today"],poms_booked,poms_left_today=do_today(task,poms_booked,poms_left_today)
    return tasks_list
    # if do_today_bool:
        # print("You should do this today:",task["content"])

def snooze(task):
    delayed_time=(datetime.today()+timedelta(days = 1)).strftime("%Y-%m-%d")
    other_api.update_task(task_id=task["id"],due_date=delayed_time)
