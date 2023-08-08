import random
import pandas as pd
import django
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ToDoList.settings')
django.setup()

from django.contrib.auth.models import User
from home.models import Task
from django.core.exceptions import ImproperlyConfigured




def save_data():
    print("Please wait.... It will take some time.")
    sample_names = ["Liam Anderson", "Emma Martinez", "Noah Johnson", "Olivia Thompson", "Ethan Williams", "Ava Garcia", "Mason Smith", "Sophia Rodriguez", "Logan Brown", "Isabella Lee", "Lucas Davis", "Mia Wilson", "Jackson Martinez", "Amelia Adams", "Aiden Scott", "Harper King", "Elijah Turner", "Charlotte Hernandez", "Caleb Green", "Abigail Perez", "Henry Campbell", "Emily White", "Samuel Flores", "Ella Mitchell", "Benjamin Turner", "Grace Lewis", "Alexander Martin", "Chloe Cooper", "Daniel Evans", "Lily Ramirez"]
    task_status = [0,1,2]
    df = pd.read_excel('C:/swapnil/TaskPriorityData.xlsx')
    df_task_desc = list(df['Task Description'])
    df_task_title = [i.split(' ')[:3] for i in df_task_desc]
    df_task_title = [i[0]+' '+i[1]+' '+i[2] for i in df_task_title]
    df_task_priority = list(df['Task Priority'])
    sample_email = []
    sample_password = []
    for name in sample_names:
        first_name, last_name = name.lower().split()
        email = f"{first_name}.{last_name}@example.com"
        password = f"{last_name}@123"
        sample_email.append(email)
        sample_password.append(password)
    for i in range(len(sample_names)):
        myuser = User.objects.create_user(sample_names[i], sample_email[i], sample_password[i])
        myuser.save()
        r1=random.randint(1,30)
        for _ in range(r1):
            new_task = Task()
            new_task.userName = sample_names[i]
            new_task.eMail = sample_email[i]
            r2=random.randint(0,len(df_task_title)-1)
            r3=random.randint(0,2)
            new_task.taskStatus = task_status[r3]
            new_task.taskTitle = df_task_title[r2]
            new_task.taskDesc = df_task_desc[r2]
            new_task.taskPriority = df_task_priority[r2]
            new_task.save()

    print("Successfully created and saved 30 user accounts and their details !!!")


if __name__ == "__main__":
    try:

        # Call the function to save data
        save_data()
    except ImproperlyConfigured as e:
        print("Error:", e)
        print("Make sure you are running this script within a Django project context.")
