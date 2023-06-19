from django.shortcuts import render, HttpResponse
from home.models import Task

# Create your views here.

def home(request):
    context = {'success':False, 'failed':False}
    if request.method == "POST":
        # Handling the form
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        if not title and not desc:
            context = {'failed':True}
        else:
            if not title:
                ins = Task(taskTitle=None, taskDesc=desc)
            elif not desc:
                ins = Task(taskTitle=title, taskDesc=None)
            else:  
                ins = Task(taskTitle=title, taskDesc=desc)
            ins.save()
            context = {'success':True}
    return render(request, 'index.html', context)


def tasks(request):
    context = {'deleted_success':False, 'updated_success':False}
    if request.method == "POST":
        deleteId = request.POST.get('deleteTaskId')
        updateId = request.POST.get('updateTask')
        if deleteId:
            Task.objects.filter(taskId=deleteId).delete()
            context['deleted_success']=True
        if updateId:
            newTitle = request.POST.get('newTitle')
            newDesc = request.POST.get('newDesc')
            context['updated_success']=True
            if not newTitle and not newDesc:
                Task.objects.filter(taskId=updateId).update(taskTitle=None, taskDesc=None)
            elif newTitle and not newDesc:
                Task.objects.filter(taskId=updateId).update(taskTitle=newTitle, taskDesc=None)
            elif not newTitle and newDesc:
                Task.objects.filter(taskId=updateId).update(taskTitle=None, taskDesc=newDesc)
            else:
                Task.objects.filter(taskId=updateId).update(taskTitle=newTitle, taskDesc=newDesc)
    else:
        if request.GET.get('status') == '1':
            Task.objects.filter(taskId=request.GET.get('Id')).update(taskStatus=1)
        elif request.GET.get('status') == '2':
            Task.objects.filter(taskId=request.GET.get('Id')).update(taskStatus=2)
        else:
            Task.objects.filter(taskId=request.GET.get('Id')).update(taskStatus=0)

    allTasks = Task.objects.all()
    context['tasks']=allTasks
    return render(request, 'tasks.html', context)


def UpdateTask(request):
    TaskId = request.POST.get('updateTaskId')
    task = Task.objects.get(taskId=TaskId)
    update_task_title = task.taskTitle
    update_task_description = task.taskDesc
    return render(request, 'UpdateTask.html', {'updateTaskTitle':update_task_title, 'updateTaskDescription':update_task_description, 'updateTaskId':TaskId})
