from django.shortcuts import render, HttpResponse, redirect
from home.models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from home.models import Contact

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


# Textutil Code

def textutil(request):
    if request.user.is_authenticated:
        return render(request, 'textutil.html')
    else:
        return HttpResponse('404 - Not Found')

def textutilAnalyze(request):
    if request.user.is_authenticated:
        djtext = request.POST.get('text', 'default')
        removepunc = request.POST.get('removepunc', 'off')
        fullcaps = request.POST.get('fullcaps', 'off')
        newlineremover = request.POST.get('newlineremover', 'off')
        extraspaceremover = request.POST.get('extraspaceremover', 'off')
        purpose = ''
        if removepunc=="on":
            analyzed = ""
            punctuations = '''.,?!;:\"'()[]{}...-—/\\&*#$%@+-=<>_|~•#'''
            for char in djtext:
                if char not in punctuations:
                    analyzed = analyzed+char
            djtext = analyzed
            if len(purpose)>0:
                purpose = purpose + ", Removed Punctutaions"
            else:
                purpose = purpose + "Removed Punctutaions"
        if fullcaps == 'on':
            analyzed = ''
            for char in djtext:
                analyzed = analyzed + char.upper()
            djtext = analyzed
            if len(purpose)>0:
                purpose = purpose + ", Capitalized"
            else:
                purpose = purpose + "Capitalized"
        if newlineremover=='on':
            analyzed = ''
            for char in djtext:
                if char !='\n' and char!='\r':
                    analyzed = analyzed + char
            djtext = analyzed
            if len(purpose)>0:
                purpose = purpose + ", New Line Removed"
            else:
                purpose = purpose + "New Line Removed"
        if extraspaceremover=='on':
            analyzed = ''
            for index, char in enumerate(djtext):
                if index<len(djtext)-1:
                    if not (djtext[index]==' ' and djtext[index+1]==' '):
                        analyzed = analyzed + char
                else:
                    analyzed = analyzed + char
            djtext = analyzed
            if len(purpose)>0:
                purpose = purpose + ", Removed ExtraSpace"
            else:
                purpose = purpose + "Removed ExtraSpace"
        if removepunc!="on" and fullcaps != 'on' and newlineremover!='on' and extraspaceremover!='on' and len(djtext)>0:
            # return HttpResponse("Please choose atleast one option")
            return render(request, 'analyze.html', {'purpose':'', 'analyzed_text':"Please choose atleast one option"})
        if len(djtext)==0:
            return render(request, 'analyze.html', {'purpose':'', 'analyzed_text':"You did'nt gave any text"})
        
        params = {'purpose':purpose, 'analyzed_text':djtext}
        return render(request, 'textutilAnalyze.html', params)
    else:
        return HttpResponse('404 - Not Found')
    

#  Icecream Shop code


def icecreamHome(request):
    if request.user.is_authenticated:
        context = {'variable': '22'}
        return render(request, 'IcecreamShopHome.html', context)
    else:
        return HttpResponse('404 - Not Found')


def icecreamAbout(request):
    if request.user.is_authenticated:
        return render(request, 'IcecreamShopAbout.html')
    else:
        return HttpResponse('404 - Not Found')


def icecreamServices(request):
    if request.user.is_authenticated:
        return render(request, 'IcecreamShopServices.html')
    else:
        return HttpResponse('404 - Not Found')


def icecreamContact(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            desc = request.POST.get('desc')
            contact = Contact(name=name, email=email, phone=phone,
                            desc=desc, date=datetime.today())
            contact.save()
            messages.success(request, 'Your message has been sent !')
            messages.success(request, 'Thankyou for reaching us.')
            messages.success(request, 'Our team will contact you')

        return render(request, 'IcecreamShopContact.html')
    else:
        return HttpResponse('404 - Not Found')


# CodeX Blog code

def CodeXhome(request):
    if request.user.is_authenticated:
        return render(request, 'codexHome.html')
    else:
        return HttpResponse('404 - Not Found')

def CodeXcontact(request):
    if request.user.is_authenticated:
        return render(request, 'codexContact.html')
    else:
        return HttpResponse('404 - Not Found')

def CodeXabout(request):
    if request.user.is_authenticated:
        return render(request, 'codexAbout.html')
    else:
        return HttpResponse('404 - Not Found')

