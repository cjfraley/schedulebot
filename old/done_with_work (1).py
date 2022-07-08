import yaml
from todoist_helper.utils.td_utilities import *

api = get_api()

def api_item_has_parent(item):
    if "parent_id" in item and item["parent_id"] is not None:
        return item["parent_id"]
    else:
        return False

if __name__ == '__main__':
    tasks=get_due_tasks()
    projects=get_projects()
    for task in tasks:
        # Get the project id of the task
        project_id=task["project_id"]
        has_parent=True
        while has_parent:
            project=api.projects.get(project_id)["project"]
            if project["name"]=="WORK":
                push_to_tomorrow(task)
                has_parent=False
                break
            else:
                project_id=api_item_has_parent(project)
                if not project_id:
                    break
    api.sync