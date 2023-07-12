from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeRegressor
from joblib import dump
import pandas as pd

task = pd.read_excel("TaskPriorityData.xlsx")

# Initialize the vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the task descriptions into numerical features
task_features = vectorizer.fit_transform(task['Task Description'])
task_label = task['Task Priority']

# Save the vectorizer as a separate joblib file
dump(vectorizer, 'TfidfVectorizer.joblib')

# Train the model
model = DecisionTreeRegressor()
model.fit(task_features, task_label)

# Save the trained model as a joblib file
dump(model, 'taskPriority.joblib')
