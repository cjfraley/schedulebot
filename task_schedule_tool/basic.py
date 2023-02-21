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

output_headings=["id","content","do_today","priority","tag_names",'child_order', 'responsible_uid', 'assigned_by_uid', 'date_added', 'checked', 'parent_id', 'day_order', 'due', 'user_id', 'is_deleted', 'sync_id', 'section_id', 'added_by_uid', 'labels', 'project_id','description', 'date_completed', 'in_history', 'has_more_notes', 'collapsed',"tags_to_add"]


# due_tasks=sorted(due_tasks, key=itemgetter('priority'), reverse=True)
priority_split_tasks=[ [] for i in range(5)]

for task in due_tasks:
    priority_split_tasks[task["priority"]].append(task)

for priority in priority_split_tasks:
    priority=sorted(priority, key=lambda x: x["due"]["date"], reverse=False)

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
    writer = csv.DictWriter(csvfile, fieldnames=output_headings)
    writer.writeheader()
    for task in due_tasks:
        writer.writerow(task)
# handle_today=[]
# for task in due_tasks_with_tag_names:
#     if
for task in due_tasks:
    if not task["do_today"]:
        if "content" in task:
            print("Snoozing %s"%task["content"])
        else:
            print(yaml.dump(task))
        snooze(task)
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
