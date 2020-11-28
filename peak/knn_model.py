# imports
import pickle
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

# functionize trainig
def train_knn(df):
    '''Train the model'''
    features_names = ['scaled_tempo', 'scaled_loudness', 'danceability', 'energy'] # 'scaled_year', 'popularity_binned'
    X = df[features_names]
    y = df['track_id']
    model = KNeighborsRegressor(algorithm='kd_tree', n_jobs=-1).fit(X, y)
    return model

# train model
model = train_knn(filtered_results)
# pickle model
with open("knn_trained.pkl", "wb") as file:
    pickle.dump(model, file)
