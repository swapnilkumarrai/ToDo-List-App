from django.shortcuts import render, HttpResponse, redirect
from home.models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from home.models import Contact
from joblib import load
import openai
from decouple import config
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use Agg backend
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import os
import plotly.express as px


# Create your views here.


# -------------------------------------------Signin/Signup--------------------------------------------


def SigninSignup(request):      # Function to render Signin/Signup page
    stored_messages = messages.get_messages(request)
    success_message = ''
    error_message = ''
    for msg in stored_messages:
        if 'successfully' in str(msg).lower():
            success_message = msg
        else:
            error_message = msg  
    return render(request, 'Signin-Signup.html', {"success_messages":success_message, "error_messages": error_message})


# ----------------------------------------CODE BASE TO HANDLE TODO APPLICATION--------------------------------------------


def home(request):      # This will render the main home page of ToDo App.
    stored_messages = messages.get_messages(request)
    success_message = ''
    for msg in stored_messages:
        success_message = msg
    if request.user.is_authenticated:
        username = request.user
        username1 = str(username).capitalize()
        context = {'success':False, 'failed':False, 'success_messages': success_message, 'username':username1}
        if request.method == "POST":
            # Handling the form
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            user = str(username)
            if not title and not desc:
                context = {'failed':True}
            else:
                model1 = load('static/ModelTrainingCode/taskPriority.joblib')
                model2 = load('static/ModelTrainingCode/tasktype.joblib')
                vectorizer = load('static/ModelTrainingCode/TfidfVectorizer.joblib')
                if not title:
                    prediction_feature = vectorizer.transform([desc])    #  Here I am using a ML model to predict the task priority based on the task description
                    predict_priority = model1.predict(prediction_feature)
                    predict_priority = predict_priority.item()
                    predict_type = model2.predict(prediction_feature)
                    predict_type = predict_type.item()
                    ins = Task(taskTitle=None, taskDesc=desc, userName=user, taskPriority=predict_priority, taskType=predict_type)
                elif not desc:
                    prediction_feature = vectorizer.transform([title])
                    predict_priority = model1.predict(prediction_feature)
                    predict_priority = predict_priority.item()
                    predict_type = model2.predict(prediction_feature)
                    predict_type = predict_type.item()
                    ins = Task(taskTitle=title, taskDesc=None, userName=user, taskPriority=predict_priority, taskType=predict_type)
                else:  
                    prediction_feature = vectorizer.transform([desc])
                    predict_priority = model1.predict(prediction_feature)
                    predict_priority = predict_priority.item()
                    predict_type = model2.predict(prediction_feature)
                    predict_type = predict_type.item()
                    ins = Task(taskTitle=title, taskDesc=desc, userName=user, taskPriority=predict_priority, taskType=predict_type)
                ins.save()
                context = {'success':True}
        return render(request, 'index.html', context)
    else:
        return HttpResponse('404 - Not Found')


def tasks(request):      # This will update and render the Task page
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
            if request.GET.get('Id') is not None:
                if request.GET.get('status') == '1':
                    Task.objects.filter(taskId=request.GET.get('Id')).update(taskStatus=1)  # Here I am updating the task status(completed, not started, in progress)
                elif request.GET.get('status') == '2':
                    Task.objects.filter(taskId=request.GET.get('Id')).update(taskStatus=2)
                else:
                    Task.objects.filter(taskId=request.GET.get('Id')).update(taskStatus=0)
        
        allTasks = Task.objects.filter(userName__exact=str(request.user)).order_by('taskPriority')
        context['tasks']=allTasks
        return render(request, 'tasks.html', context)   
    else:
        return HttpResponse('404 - Not Found')


def UpdateTask(request):      # This is the function to handle the update task
    if request.user.is_authenticated:
        TaskId = request.POST.get('updateTaskId')
        task = Task.objects.get(taskId=TaskId)
        update_task_title = task.taskTitle
        update_task_description = task.taskDesc
        return render(request, 'UpdateTask.html', {'updateTaskTitle':update_task_title, 'updateTaskDescription':update_task_description, 'updateTaskId':TaskId})
    else:
        return HttpResponse('404 - Not Found')


# ----------------------------------------CODE BASE TO HANDLE AUTHENTICATION--------------------------------------------


def handleSignup(request):      # This function will handle the Signup to ToDo app
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
    

def handleLogin(request):      # This function will handle the Login to ToDo app
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

def handleLogout(request):      # This function will handle the Logout
    logout(request)
    messages.success(request, "Successfully Logged Out !")
    return redirect('/')


def handleDelete(request):      # This function will handle the Delete account will all its data
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
                obj.delete()
            messages.success(request, "Successfully Deleted account !")
            return redirect('/')
        else:
            # Incorrect password
            messages.error(request, "Incorrect password, Please try again !")
            return redirect('/')
    else:
        return HttpResponse('404 - Not Found')
    


# # ----------------------------------------CODE BASE TO HANDLE TEXTUTIL WEBSITE--------------------------------------------


def textutil(request):      # This function will render the TextUtil page
    if request.user.is_authenticated:
        return render(request, 'textutil.html')
    else:
        return HttpResponse('404 - Not Found')

def textutilAnalyze(request):      # This function will handle the text analysis and render TextAnalyze page with optimised text.
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
    

#  # ----------------------------------------CODE BASE TO HANDLE ICECREAM SHOP WEBSITE--------------------------------------------


def icecreamHome(request):      # This function will return Icecream Shop home page
    if request.user.is_authenticated:
        context = {'variable': '22'}
        return render(request, 'IcecreamShopHome.html', context)
    else:
        return HttpResponse('404 - Not Found')


def icecreamAbout(request):      # This function will render Icecream shop about page.
    if request.user.is_authenticated:
        return render(request, 'IcecreamShopAbout.html')
    else:
        return HttpResponse('404 - Not Found')


def icecreamServices(request):      # This function will render Icecreamshop Services page.
    if request.user.is_authenticated:
        return render(request, 'IcecreamShopServices.html')
    else:
        return HttpResponse('404 - Not Found')


def icecreamContact(request):      # This function will render Icecream shop contact page
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


# # ----------------------------------------CODE BASE TO HANDLE CODEX BLOG WEBSITE--------------------------------------------

def CodeXhome(request):      # This function will return Codexhome page.
    if request.user.is_authenticated:
        return render(request, 'codexHome.html')
    else:
        return HttpResponse('404 - Not Found')

def CodeXcontact(request):      # This will render codex contact page
    if request.user.is_authenticated:
        return render(request, 'codexContact.html')
    else:
        return HttpResponse('404 - Not Found')

def CodeXabout(request):      # This will render Codex about page
    if request.user.is_authenticated:
        return render(request, 'codexAbout.html')
    else:
        return HttpResponse('404 - Not Found')


# # ----------------------------------------CODE BASE TO HANDLE OPENAI CHATBOT--------------------------------------------

def chatBot(request):      # This function will use openAI api and return response to the question asked. It will render AIBot.html.
    if request.user.is_authenticated:
        username = str(request.user).capitalize()
        userQuestion = ''
        axelResponse = ''
        if request.method == "POST":
            userQuestion = request.POST.get('userQuestion')
            openai.api_key = config('OPENAI_API_KEY')
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f" {userQuestion} "}])
            axelResponse = completion.choices[0].message.content

            
        context = {"userQuestion":userQuestion, "axelResponse":axelResponse, "username":username}            
        return render(request, 'AIBot.html', context)    
    else:
        return HttpResponse('404 - Not Found')



# # ----------------------------------------CODE BASE TO CREATE PROGRESS DASHBOARD--------------------------------------------

def dashboard(request):
    if request.user.is_authenticated:
        def is_file_exist(directory, filename):
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                # Delete the file if it exists
                try:
                    os.remove(file_path)
                    print(f"File '{filename}' deleted successfully.")
                except OSError as e:
                    print(f"Error: {e}")
            # Create a FigureCanvasAgg and save the plot
            canvas = FigureCanvas(plt.gcf())
            canvas.print_png(file_path)

        username = str(request.user)
        # Creating DataFrame for all users
        user_names = User.objects.all()
        user_names = [user.username for user in user_names]
        total_tasks = [Task.objects.filter(userName__exact=name).count() for name in user_names]
        completed_tasks = [Task.objects.filter(userName__exact=name, taskStatus=1).count() for name in user_names]
        tasks_completion_rate = [((completed_tasks[i] / total_tasks[i]) * 100) if total_tasks[i]>0 else 0 for i in range(len(total_tasks))]
        All_Users = pd.DataFrame({'User_Names':user_names, 'Total_Tasks':total_tasks, 'Completed_Tasks':completed_tasks, 'Tasks_Completion_Rate':tasks_completion_rate})

        # Creating DataFrame for every individual
        individual_query_set = Task.objects.filter(userName__exact=username)
        tasks_id = individual_query_set.values_list('taskId', flat=True)
        tasks_status = individual_query_set.values_list('taskStatus', flat=True)
        tasks_priority = individual_query_set.values_list('taskPriority', flat=True)
        Individual_User = pd.DataFrame({'Task_Ids':tasks_id, 'Task_Status':tasks_status, 'Task_Priority':tasks_priority})

        # Pie Chart
        plt.pie(Individual_User['Task_Status'].value_counts().values, labels=['Completed' if i==2 else 'In Progress' if i==1 else 'Not Started' for i in list(Individual_User['Task_Status'].value_counts().index)], autopct='%0.1f%%', explode=[0.1 if i==2 else 0 for i in list(Individual_User['Task_Status'].value_counts().index)])
        plt.title('Your Task Progress using Pie Chart')
        plt.axis('equal')
        is_file_exist('static/Dashboard/', f'progress_pie_chart_{username}.png')
        plt.close()

        # Bar Chart
        plt.bar(list(np.sort(Individual_User['Task_Priority'].unique())), [Individual_User[(Individual_User['Task_Priority']==i) & (Individual_User['Task_Status']==2)].shape[0] for i in range(1, 6)], color=['red', 'blue', 'green', 'orange', 'purple'])
        plt.title('Your Task Priority insights using Bar Chart')
        plt.xlabel('Task Priorities where 1 is most important and 5 is least important')
        plt.ylabel('Task Completed')
        is_file_exist('static/Dashboard/', f'priority_bar_chart_{username}.png')
        plt.close()

        # Line Plot
        user_task_created = [Task.objects.filter(userName__exact=username, taskPriority=i).count() for i in range(1, 6)]
        user_task_priority = [1, 2, 3, 4, 5]
        line_plot_df = pd.DataFrame({'user_task_priority':user_task_priority, 'user_task_created':user_task_created})
        fig = px.line(line_plot_df, x='user_task_priority', y='user_task_created', title='User Task Creation per priority')
        # Convert the Plotly figure to HTML using plotly.io.to_html()
        plot_html = fig.to_html() 

        # Scatter Plot
        plt.figure(figsize=(10, 6))
        plt.scatter(All_Users['Total_Tasks'], All_Users['Tasks_Completion_Rate'], s=[i*10 for i in All_Users['Completed_Tasks']])
        for i in range(All_Users.shape[0]):
            if All_Users['User_Names'].values[i]==username:
                plt.text(All_Users['Total_Tasks'].values[i], All_Users['Tasks_Completion_Rate'].values[i], All_Users['User_Names'].values[i].split()[0], color='red')
            else:
                plt.text(All_Users['Total_Tasks'].values[i], All_Users['Tasks_Completion_Rate'].values[i], All_Users['User_Names'].values[i].split()[0])
        plt.title('Your Progress Compared To Other Users Using Scatter Plot. (marker size represents number of tasks completed)')
        plt.xlabel('Total Task created')
        plt.ylabel('Task completion rate (%)')
        plt.tight_layout()
        is_file_exist('static/Dashboard/', f'task_completion_rate_scatter_plot_{username}.png')
        plt.close()
        return render(request, 'dashboard.html', {'username':username, 'plot_html': plot_html})
    else:
        return HttpResponse('404 - Not Found')


