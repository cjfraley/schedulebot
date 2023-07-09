import yaml, json, csv
from datetime import *
from td_utilities import *
from operator import itemgetter
import todoist
import logging
logger = logging.getLogger(__name__)

try:
    specialization_object = Specialization.objects.get(name="My Test Specialization")
except Exception as ex:
    logger.info(ex, exc_info=True) # exc_info will add traceback

# https://developer.todoist.com/rest/v1/?python#get-active-tasks
if "pom_limit" in os.environ:
    allotted_time = int(os.environ["pom_limit"])
else:
    allotted_time = 5
# methods = [method_name for method_name in dir(api) if callable(getattr(api, method_name))]
api=get_api()
due_tasks=get_due_tasks()

# due_tasks_with_tag_names=[]
for task in due_tasks:
    task["tag_names"]=get_task_labels(task)

# due_tasks=sorted(due_tasks, key=itemgetter('priority'), reverse=True)
priority_split_tasks=[ [] for i in range(5)]

for task in due_tasks:
    priority_split_tasks[task["priority"]].append(task)

for priority in priority_split_tasks:
    priority=sorted(priority, key=lambda x: x["due"].date, reverse=False)

# sort by priority
    # Sort by due date

poms_left_today=5
poms_booked=0
# tasks_assessed_for_today=[]
due_tasks=[task for priority_level in reversed(priority_split_tasks) for task in priority_level]
for task in due_tasks:
    task["do_today"],poms_booked,poms_left_today=do_today(task,poms_booked,poms_left_today)
# for task in due_tasks_with_tag_names:
#     if "do_today" not in task:
#         print(yaml.dump(task))
#         exit()

with open("test_output.csv", 'w') as csvfile:
    output_headings=list(due_tasks[0].keys())+["tags_to_add"]
    writer = csv.DictWriter(csvfile, fieldnames=output_headings)
    writer.writeheader()
    for task in due_tasks:
        writer.writerow(task)
# handle_today=[]
# for task in due_tasks_with_tag_names:
#     if

rest_api=get_api(sync=False)
for task in due_tasks:
    if not task["do_today"]:
        if "content" in task:
            print("Snoozing %s"%task["content"])
        else:
            print(yaml.dump(task))
        snooze(task)
        # if task["due"].is_recurring:
        #     print("task id",task["id"])
        #     print("Pre snooze:\n",yaml.dump(task))
        #     print("Post snooze:\n",yaml.dump(rest_api.get_task(task["id"]).__dict__))
        #     exit()
api.sync()
# print(api.items.list())
# print(methods)
# for item in api.state['items']:
#     # if "object_type" in item:
#     #     print(yaml.dump(item))
#     # print(item["object_type"])
#     # for key in item:
#     #     print(key)
#     # with open("test_out.yaml","w") as test_out_file:
#     #     yaml.dump(item,test_out_file)
#     # print(yaml.dump(item))
#     print(type(item))
#     break
# for aspect in api.state:
#     print(aspect)
