# -*- coding: utf-8 -*-
"""A2_23D1269.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Lo93qOXL4qENqL8GyX_kV-s2N8mOLhiT
"""
import streamlit as st
import sys

st.write(f"Python executable: {sys.executable}")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
print("Current directory:", os.getcwd())
print("Files in current directory:", os.listdir('.'))


red = pd.read_csv('./wine+quality/winequality-red.csv', delimiter=';')

print(red.columns.tolist())

# Show the first 5 rows of the dataset
print(red.head())

# Code taken from  stack overfolw

white = pd.read_csv('./wine+quality/winequality-white.csv', delimiter=';')



column_means = red.mean()

# Printing mean of each column with its name
print("Mean of each numeric column:")
for column_name, mean_value in column_means.items():
    print(f"{column_name}: {mean_value}")
# code taken from chatgpt
# mean of each column of redwine taken

column_means = white.mean()

# Printing mean of each column with its name
print("Mean of each numeric column:")
for column_name, mean_value in column_means.items():
    print(f"{column_name}: {mean_value}")

red_means = red.mean(numeric_only=True)

mean_values_comparisonred = pd.DataFrame({'Red wine': red_means })
# Plotting
mean_values_comparisonred.plot(kind='bar', figsize=(5, 5))
plt.title('Mean Values of Characteristics: Red Wine')
plt.xlabel('Characteristics')
plt.ylabel('Mean Value')
plt.legend(title='Wine Type')
plt.show()

#label a segment of data
qualitycorrelation_data = red[['quality','alcohol','residual sugar','volatile acidity','sulphates']]

# Calculating the correlation between datasets
corr_matrix = qualitycorrelation_data.corr()

# Visualize the correlation matrix
plt.figure(figsize=(5,5))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=.4, fmt=".4f")
plt.title('Correlation of "Quality of Red wine" with different physiochemical properties')  # Chart title
plt.show()  # Show the plot

#preprocessing
#droppingMissing values
#code taken from sci-kit learn libraray
#importing the sci-kit learn library
from sklearn.model_selection import train_test_split

red = red.dropna()

#splitting the data into training and testing dataset
X = red.drop('quality', axis=1)  # Feature to be predicted
y = red['quality']  # defining the target variable

# splitting the data into train and test set
# taking 25% of data for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=25)

#since the unit of measurement of different columns varies, in order to standardise the scales I have used the code standardscaleer from scikit libraray
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

# Fit on training data
X_train_scaled = scaler.fit_transform(X_train)

# Only transform the test data
X_test_scaled = scaler.transform(X_test)

#code taken from Scikit-learn's preprocessing module

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np



rf_parameters = {'n_estimators': [250, 500], 'max_depth': [25, 50, None]}
rf_grid_search = GridSearchCV(RandomForestRegressor(random_state=25), rf_parameters, cv=10)
rf_grid_search.fit(X_train, y_train)
best_rf_model = rf_grid_search.best_estimator_
rf_predictions = best_rf_model.predict(X_test)
rf_mse = mean_squared_error(y_test, rf_predictions)



#  print  Mean squared error
print('Random Forest MSE:', rf_mse)

from sklearn.svm import SVR
svr_params = {'C': [0.1, 1, 10], 'gamma': [0.01, 0.1, 1]}
svr_grid_search = GridSearchCV(SVR(kernel='rbf'), svr_params, cv=5)
svr_grid_search.fit(X_train, y_train)
best_svr_model = svr_grid_search.best_estimator_
svr_predictions = best_svr_model.predict(X_test)
svr_mse = mean_squared_error(y_test, svr_predictions)
#  print  MSE for
print('SVM MSE:', svr_mse)

importances = best_rf_model.feature_importances_
import matplotlib.pyplot as plt

features = X_train.columns
indices = np.argsort(importances)

plt.title('Feature Importances in Random Forest')
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel('Relative Importance')
plt.show()

from sklearn.inspection import permutation_importance

# Train the SVM model
svr = SVR(kernel='rbf', C=1, gamma=0.1)
svr.fit(X_train, y_train)

# Compute Permutation Feature Importance
perm_importance = permutation_importance(svr, X_test, y_test, n_repeats=30, random_state=42)

# Plotting
sorted_idx = perm_importance.importances_mean.argsort()
plt.figure(figsize=(4, 4))
plt.barh(range(X_train.shape[1]), perm_importance.importances_mean[sorted_idx])
plt.yticks(range(X_train.shape[1]), X_train.columns[sorted_idx])
plt.title("Permutation Importance with SVM")
plt.show()

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Split the datasets
X_red = red.drop('quality', axis=1)
y_red = red['quality']
X_white = white.drop('quality', axis=1)
y_white = white['quality']

# Train a model for red wine
red_model = RandomForestRegressor()
red_model.fit(X_red, y_red)

# Train a model for white wine
white_model = RandomForestRegressor()
white_model.fit(X_white, y_white)

# Test the red model with white wine data
red_predictions_on_white = red_model.predict(X_white)
mse_red_on_white = mean_squared_error(y_white, red_predictions_on_white)

# Test the white model with red wine data
white_predictions_on_red = white_model.predict(X_red)
mse_white_on_red = mean_squared_error(y_red, white_predictions_on_red)

# Print the MSE for comparison
print("MSE of red wine model on white wine data:", mse_red_on_white)
print("MSE of white wine model on red wine data:", mse_white_on_red)

from sklearn.ensemble import RandomForestRegressor
import joblib

# Example: Training a model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Saving the model to a file
model_path = 'random_forest_model.pkl'  # The file path and name where you want to save your model
joblib.dump(model, model_path)

              
"""# New Section"""
import pickle
# Import necessary libraries
import streamlit as st
import numpy as np
import joblib

# Load the pre-trained model (ensure this model file exists in your directory)
model_path = 'random_forest_model.pkl'  # Adjust the path if your model is located elsewhere
model = joblib.load(model_path)

# Streamlit app title
st.title('Wine Quality Prediction App')

# Description or caption
st.write('This app predicts the quality of wine based on various physicochemical properties.')

# User inputs through sliders
fixed_acidity = st.slider('Fixed Acidity', min_value=4.0, max_value=16.0, value=8.0, step=0.1)
volatile_acidity = st.slider('Volatile Acidity', min_value=0.0, max_value=2.0, value=0.5, step=0.01)
citric_acid = st.slider('Citric Acid', min_value=0.0, max_value=1.0, value=0.25, step=0.01)
residual_sugar = st.slider('Residual Sugar', min_value=0.0, max_value=15.0, value=2.5, step=0.1)
chlorides = st.slider('Chlorides', min_value=0.0, max_value=0.2, value=0.05, step=0.001)
free_sulfur_dioxide = st.slider('Free Sulfur Dioxide', min_value=1, max_value=72, value=15)
total_sulfur_dioxide = st.slider('Total Sulfur Dioxide', min_value=6, max_value=289, value=46)
density = st.slider('Density', min_value=0.990, max_value=1.003, value=0.996, step=0.0001)
pH = st.slider('pH', min_value=2.8, max_value=4.0, value=3.3, step=0.01)
sulphates = st.slider('Sulphates', min_value=0.3, max_value=2.0, value=0.5, step=0.01)
alcohol = st.slider('Alcohol', min_value=8.0, max_value=14.0, value=10.5, step=0.1)

# Arrange user inputs into feature array
# Ensure the order of these features matches the order expected by your model
features = np.array([[fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
                      chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density,
                      pH, sulphates, alcohol]])

# Predict button
if st.button('Predict Quality'):
    prediction = model.predict(features)
    st.write(f'The predicted quality is: {prediction[0]}')

