from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump
import pandas as pd


print("Please wait, your model is getting ready..............")
task = pd.read_excel("C:/swapnil/ToDoList/static/ModelTrainingCode/TaskPriorityData.xlsx")

# Initialize the vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the task descriptions into numerical features
task_features = vectorizer.fit_transform(task['Task Description'])
task_label = task['Task Priority']
task_type = task['Task Type']

# Save the vectorizer as a separate joblib file
dump(vectorizer, 'TfidfVectorizer.joblib')

# Train the model to predict Task Priority
model1 = DecisionTreeRegressor()
model1.fit(task_features, task_label)

# Train the model to predict Task Type
model2 = KNeighborsClassifier()
model2.fit(task_features, task_type)

# Save the trained model as a joblib file
dump(model1, 'taskPriority.joblib')
dump(model2, 'tasktype.joblib')
print('model is trained and ready to use ')
