# BOTbet
Here are the highlights of the code:

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
