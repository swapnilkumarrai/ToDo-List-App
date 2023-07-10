from django.shortcuts import render, HttpResponse, redirect
from home.models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def SigninSignup(request):
    stored_messages = messages.get_messages(request)
    success_message = ''
    error_message = ''
    for msg in stored_messages:
        if 'successfully' in str(msg).lower():
            success_message = msg
        else:
            error_message = msg 
    print("opm", success_message)           
    return render(request, 'Signin-Signup.html', {"success_messages":success_message, "error_messages": error_message})

def home(request):
    stored_messages = messages.get_messages(request)
    success_message = ''
    for msg in stored_messages:
        success_message = msg
    print("balze", request.user)
    if request.user.is_authenticated:
        username = request.user
        username = str(username).capitalize()
        context = {'success':False, 'failed':False, 'success_messages': success_message, 'username':username}
        if request.method == "POST":
            # Handling the form
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            user = str(username)
            if not title and not desc:
                context = {'failed':True}
            else:
                if not title:
                    ins = Task(taskTitle=None, taskDesc=desc, userName=user)
                elif not desc:
                    ins = Task(taskTitle=title, taskDesc=None, userName=user)
                else:  
                    ins = Task(taskTitle=title, taskDesc=desc, userName=user)
                ins.save()
                context = {'success':True}
        return render(request, 'index.html', context)
    else:
        return HttpResponse('404 - Not Found')


def tasks(request):
    if request.user.is_authenticated:
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
            print("hello1", request.GET.get('Id'))
            if request.GET.get('Id') is not None:
                print("hello2")
                if request.GET.get('status') == '1':
                    Task.objects.filter(taskId=request.GET.get('Id')).update(taskStatus=1)
                elif request.GET.get('status') == '2':
                    Task.objects.filter(taskId=request.GET.get('Id')).update(taskStatus=2)
                else:
                    Task.objects.filter(taskId=request.GET.get('Id')).update(taskStatus=0)

        allTasks = Task.objects.filter(userName__exact=str(request.user))
        context['tasks']=allTasks
        return render(request, 'tasks.html', context)
    else:
        return HttpResponse('404 - Not Found')


def UpdateTask(request):
    if request.user.is_authenticated:
        TaskId = request.POST.get('updateTaskId')
        task = Task.objects.get(taskId=TaskId)
        update_task_title = task.taskTitle
        update_task_description = task.taskDesc
        return render(request, 'UpdateTask.html', {'updateTaskTitle':update_task_title, 'updateTaskDescription':update_task_description, 'updateTaskId':TaskId})
    else:
        return HttpResponse('404 - Not Found')


def handleSignup(request):
    if request.method =='POST':
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous inputs
        if len(username)>10:
            messages.error(request, "Username must be under 10 characters !")
            return redirect('/')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exist. Please choose a different Username !")
            return redirect('/')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exist. Please choose a different Email-id !")
            return redirect('/')
        
        if not username.isalnum():
            messages.error(request, "Username should only contain alphabets and numbers !")
            return redirect('/')
        
        if pass1!=pass2:
            messages.error(request, "Passwords do not match !")
            return redirect('/')

        # Create user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "Your ToDo account has been successfully created !")
        return  redirect('/')
    else:
        return HttpResponse('404 - Not Found')  
    

def handleLogin(request):
    if request.method =='POST':
        # Get the post parameters
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user:
            login(request ,user)
            messages.success(request, "Successfully Logged In !")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again !")
            return redirect('/')
    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out !")
    return redirect('/')


def handleDelete(request):
    if request.method =='POST':
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if pass1!=pass2:
            messages.error(request, "Passwords do not match !")
            return redirect('/')
        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            # User with the provided username and email doesn't exist
            messages.error(request, "User with the provided username and email doesn't exist !")
            return redirect('/')

        # Check if the provided password matches the user's password
        if user.check_password(pass2):
            # Delete the User account
            user.delete()
            obj = Task.objects.filter(userName__exact=username)
            if obj.exists():
                print("goku", obj)
                obj.delete()
            messages.success(request, "Successfully Deleted account !")
            return redirect('/')
        else:
            # Incorrect password
            messages.error(request, "Incorrect password, Please try again !")
            return redirect('/')
    else:
        return HttpResponse('404 - Not Found')
