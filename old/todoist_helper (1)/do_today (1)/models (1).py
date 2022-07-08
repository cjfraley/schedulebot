from django.db import models
import ast, yaml, json
# Create your models here.
# class TasksList(models.Model):
#     content=

class ListField(models.TextField):
    # https://stackoverflow.com/questions/22340258/django-list-field-in-model
    # __metaclass__= models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class Task(models.Model):
    id =  models.IntegerField(primary_key=True)
    content = models.CharField(max_length=200)
    do_today = models.BooleanField()
    priority =  models.IntegerField()
    tag_names = ListField()
    child_order =  models.IntegerField()
    responsible_uid =  models.IntegerField()
    assigned_by_uid =  models.IntegerField()
    date_added = models.DateTimeField()
    checked = models.BooleanField()
    parent_id =  models.IntegerField()
    day_order =  models.IntegerField()
    due = models.BooleanField()
    user_id =  models.IntegerField()
    is_deleted = models.BooleanField()
    sync_id =  models.IntegerField()
    section_id =  models.IntegerField()
    added_by_uid =  models.IntegerField()
    labels  = ListField()
    project_id =  models.IntegerField()
    date_completed = models.DateTimeField()
    in_history = models.BooleanField()
    has_more_notes = models.BooleanField()
    collapsed = models.BooleanField()
    tags_to_add = ListField()
    last_synched = models.DateTimeField()
    raw = models.CharField(max_length=1000)
    def __str__(self):
        return json.dumps({"id":id, "content":content})

class Query(models.Model):
    """Enables interactive selection of tasks."""

    def __init__(self, arg):
        super(Query, self).__init__()
        self.arg = arg
