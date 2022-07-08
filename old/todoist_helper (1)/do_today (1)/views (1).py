from django.shortcuts import render
from django.http import HttpResponse
from utils.td_utilities import *
from django.shortcuts import render
import re
# Create your views here.
def index(request):
    output_string=""
    task_list = what_today()
    delayed_tasks = []
    # template = loader.get_template('do_today/index.html')
    output_list=[]
    for task in what_today():
        if task["do_today"]:
            output_list.append(task)
            # output_string+="<\br>"
        else:
            delayed_tasks.append(task)
    fix_links(output_list)
    fix_links(delayed_tasks)
    context = {
        "task_list": output_list,
        "delayed_tasks": delayed_tasks,
        "projects": get_projects(),
        "project": "all"
    }
    return HttpResponse(render(request,'do_today/index.html',context))

def fix_links(list_of_tasks):
    for task in list_of_tasks:
        # print("Nothing")
        task["content"]=re.sub("\[(.*)\]\((.*)\)",'<a href="\g<2>">\g<1></a>',task["content"])
    return list_of_tasks
