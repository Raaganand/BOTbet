# -*- coding: utf-8 -*-
"""Project_2_Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15-aUHdxKUSsctFkvhIYAtHyfjD9yNTzF
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
df = pd.read_csv('2019.csv')

# Convert the date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Extract the year component
df['Year'] = df['Date'].dt.year

# Drop the original date and unwanted columns
df.drop(['Date', 'Year', 'B365A', 'B365H', 'B365D'], axis=1, inplace=True)

# Select the categorical columns
categorical_columns = ['HomeTeam', 'AwayTeam', 'Referee']

# Perform label encoding on the categorical columns
label_encoder = LabelEncoder()
for column in categorical_columns:
    df[column] = label_encoder.fit_transform(df[column])

# Create a new column 'Result' based on conditions
df['Result'] = df.apply(lambda row: 0 if row['Away_Score'] > row['Home_Score'] else (1 if row['Home_Score'] > row['Away_Score'] else 2), axis=1)

# Drop the 'Div' column
df.drop('Div', axis=1, inplace=True)

# Select the columns to be standardized
columns_to_standardize = ['Home_Score', 'Away_Score']

# Perform standardization
scaler = StandardScaler()
df[columns_to_standardize] = scaler.fit_transform(df[columns_to_standardize])

# Save the modified DataFrame to CSV
df.to_csv('label_encoded.csv', index=False)

# Save the label encoder and scaler
joblib.dump(label_encoder, 'team_encoder.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Read the data from the CSV file
data = pd.read_csv('label_encoded.csv')

# Split the data into input features (X) and output feature (y)
X = data[['HomeTeam', 'AwayTeam', 'Home_Score', 'Away_Score', 'Referee']]
y = data['Result']

# Split the data into training and testing sets (e.g., 80% training, 20% testing)
train_size = int(0.8 * len(data))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Train the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Train the SVM model
svm_model = SVC(kernel='rbf', random_state=42)
svm_model.fit(X_train, y_train)

# Save the trained models
joblib.dump(rf_model, 'random_forest_model.pkl')
joblib.dump(svm_model, 'svm_model.pkl')

# Make predictions using the ensemble model
rf_predictions = rf_model.predict(X_test)
svm_predictions = svm_model.predict(X_test)
ensemble_predictions = (rf_predictions + svm_predictions) // 2  # Voting/averaging

# Evaluate the performance of the ensemble model
accuracy = accuracy_score(y_test, ensemble_predictions)
precision = precision_score(y_test, ensemble_predictions, average='weighted')
recall = recall_score(y_test, ensemble_predictions, average='weighted')
f1 = f1_score(y_test, ensemble_predictions, average='weighted')
confusion = confusion_matrix(y_test, ensemble_predictions)

print("Ensemble Model Performance:")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:")
print(confusion)

# Create a heatmap of the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Load the trained models and label encoders
rf_model = joblib.load('random_forest_model.pkl')
svm_model = joblib.load('svm_model.pkl')
team_encoder = joblib.load('team_encoder.pkl')
scaler = joblib.load('scaler.pkl')

# Read the data from the CSV file
data = pd.read_csv('label_encoded.csv')

# Split the data into input features (X) and output feature (y)
X = data[['HomeTeam', 'AwayTeam', 'Home_Score', 'Away_Score', 'Referee']]
y = data['Result']

# Apply preprocessing steps to the test data
X_test = X[train_size:]
y_test = y[train_size:]

# Standardize the features using the pre-trained scaler
columns_to_standardize = ['Home_Score', 'Away_Score']
X_test[columns_to_standardize] = scaler.transform(X_test[columns_to_standardize])

# Make predictions using the ensemble model
rf_predictions = rf_model.predict(X_test)
svm_predictions = svm_model.predict(X_test)
ensemble_predictions = (rf_predictions + svm_predictions) // 2  # Voting/averaging

# Map the predicted values back to original labels
result_mapping = {0: 'Loss', 1: 'Win', 2: 'Draw'}
ensemble_predictions = [result_mapping[prediction] for prediction in ensemble_predictions]

# Compare the predictions with the actual labels
predictions_df = pd.DataFrame({'Actual': y_test, 'Predicted': ensemble_predictions})

# Print the predictions
print(predictions_df)

# Visualize the comparison of actual and predicted labels
plt.figure(figsize=(12, 6))
sns.countplot(x='Actual', hue='Predicted', data=predictions_df)
plt.title('Comparison of Actual and Predicted Labels')
plt.xlabel('Actual')
plt.ylabel('Count')
plt.legend(title='Predicted')
plt.show()

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

# Load the trained models and label encoders
rf_model = joblib.load('random_forest_model.pkl')
svm_model = joblib.load('svm_model.pkl')
team_encoder = joblib.load('team_encoder.pkl')
scaler = joblib.load('scaler.pkl')

# Define the original team names
home_team_name = input("Enter the name of the home team: ")
away_team_name = input("Enter the name of the away team: ")

# Add missing team names to the label encoder
team_encoder.classes_ = np.append(team_encoder.classes_, [home_team_name, away_team_name])

# Map the original team names to encoded values
home_team_encoded = team_encoder.transform([home_team_name])[0]
away_team_encoded = team_encoder.transform([away_team_name])[0]

# Create a DataFrame for prediction
prediction_data = pd.DataFrame({
    'HomeTeam': [home_team_encoded],
    'AwayTeam': [away_team_encoded],
    'Home_Score': [0],  # Example value, provide the actual home score
    'Away_Score': [0],  # Example value, provide the actual away score
    'Referee': [0]  # Example value, provide the actual referee encoded value
})

# Apply preprocessing steps to the prediction data
prediction_data = prediction_data.astype(float)  # Ensure data type is float

# Standardize the features using the pre-trained scaler
columns_to_standardize = ['Home_Score', 'Away_Score']
prediction_data[columns_to_standardize] = scaler.transform(prediction_data[columns_to_standardize])

# Make predictions using the ensemble model
rf_predictions = rf_model.predict(prediction_data)
svm_predictions = svm_model.predict(prediction_data)
ensemble_predictions = (rf_predictions + svm_predictions) // 2  # Voting/averaging

# Map the predicted values back to original labels
result_mapping = {0: 'Loss', 1: 'Win', 2: 'Draw'}
predicted_result = result_mapping[ensemble_predictions[0]]

# Print the predicted result
print(f"The predicted result for {home_team_name} vs {away_team_name} is Home_team: {predicted_result}")

"""Here are the highlights of the code:

Data Preparation and Preprocessing:

The code reads a CSV file containing football match data.
The date column is converted to datetime format, and the year component is extracted.
Unwanted columns (e.g., 'Date', 'Year', 'B365A', 'B365H', 'B365D') are dropped.
Categorical columns ('HomeTeam', 'AwayTeam', 'Referee') are label encoded using LabelEncoder.
A new column 'Result' is created based on the home and away scores.
The 'Div' column is dropped, and the 'Home_Score' and 'Away_Score' columns are standardized using StandardScaler.
The modified DataFrame is saved to a new CSV file, and the label encoder and scaler are saved using joblib.
Model Training:

The code splits the preprocessed data into input features (X) and output feature (y).
The data is further split into training and testing sets (80% training, 20% testing).
Two models are trained: Random Forest and Support Vector Machine (SVM).
The trained models are saved using joblib.
Ensemble Model and Evaluation:

The code combines the predictions of the Random Forest and SVM models using voting/averaging.
The performance of the ensemble model is evaluated using metrics like accuracy, precision, recall, and F1 score.
A confusion matrix is generated to visualize the performance.
Visualization:

The code creates a heatmap of the confusion matrix using matplotlib and seaborn.
It also plots a countplot to compare the actual and predicted labels.
Making Predictions:

The code loads the trained models, label encoders, and scaler.
User input is taken for the names of the home and away teams.
The input team names are added to the label encoder and mapped to encoded values.
A prediction DataFrame is created based on the input team names and example values for home score, away score, and referee.
The prediction data is preprocessed and standardized.
Predictions are made using the ensemble model, and the predicted result is mapped back to the original labels.
The predicted result is printed.
"""

The confusion matrix you provided has three rows and three columns, representing the actual and predicted labels for three classes: Loss, Win, and Draw.

Here's a breakdown of the confusion matrix:

The first row indicates the actual labels of the Loss class. In this case, there were 92 instances of the Loss class, and the model correctly predicted all of them as Loss (true negatives). There were 3 instances of the Loss class that the model incorrectly predicted as Win (false positives), meaning the model made 3 errors in predicting Loss.
The second row represents the actual labels of the Win class. Out of 88 instances of the Win class, the model correctly predicted 87 of them as Win (true positives). There was 1 instance of the Win class that the model incorrectly predicted as Loss (false negative), indicating one error in predicting Win.
The third row corresponds to the actual labels of the Draw class. Among 45 instances of the Draw class, the model correctly predicted 4 of them as Draw (true positives). However, there were 41 instances of the Draw class that the model incorrectly predicted as Win (false negatives), resulting in 41 errors in predicting Draw.
In summary, the confusion matrix provides a breakdown of the model's performance for each class. It allows us to evaluate the accuracy and errors of the model's predictions for different classes.