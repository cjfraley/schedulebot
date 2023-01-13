from google.cloud import bigquery
import yaml, json, csv
from datetime import *
from td_utilities import *

if __name__=="__main__":
    client = bigquery.Client()
    # Get Todoist Info
    events=get_relevant_td_activities()
    # TODO get last event in bq
    # Upload all later events to bq
    # dataset = client.create_dataset('general-tracking-370719.TaskTracking')
    # table = dataset.table('')
    table_ref = 'general-tracking-370719.TaskTracking.TodoEvents'# client.dataset('general-tracking-370719.TaskTracking').table('TodoEvents')
    table = client.get_table(table_ref)
    
    job_config = bigquery.job.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField('id', 'STRING'),# 	The ID of the event.
        bigquery.SchemaField('object_type', 'STRING'),# 	The type of object, one of item, note or project.
        bigquery.SchemaField('object_id', 'STRING'), # 	The ID of the object.
        bigquery.SchemaField('event_type', 'STRING'), # 	The type of event, one of added, updated, deleted, completed, uncompleted, archived, unarchived, shared, left.
        bigquery.SchemaField('event_date', 'STRING'), # 	The date and time when the event took place.
        bigquery.SchemaField('parent_project_id', 'STRING'), # 	The ID of the item's or note's parent project, otherwise null.
        bigquery.SchemaField('parent_item_id', 'STRING'), # 	The ID of the note's parent item, otherwise null.
        bigquery.SchemaField('initiator_id', 'STRING'), # 	The ID of the user who is responsible for the event, which only makes sense in shared projects, items and notes, and is null for non-shared objects.
        bigquery.SchemaField('extra_data', 'JSON'),#This object contains at least the name of the project, or the content of an item or note, and optionally the last_name if a project was renamed, the last_content if an item or note was renamed, the due_date and last_due_date if an item's due date changed, the responsible_uid and last_responsible_uid if an item's responsible uid changed, the description and last_description if an item's description changed, and the client that caused the logging of the event.
    ]
    
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    # load_job = client.insert_rows()
    # print(json.dumps(events))
    load_job = client.load_table_from_json(
        events, table_ref, job_config = job_config
    )
    print("Started load job")
    try:
        print(load_job.result())
    except:
        print("Errors:\n",load_job.errors)
