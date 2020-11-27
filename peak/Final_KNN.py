#!/usr/bin/env python
# coding: utf-8


# imports
import pickle
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor


# # load filtered dataset
# ???
# df = pd.read_csv('../raw_data/full_dataset.csv')


def get_seed_features(filtered_df):
    '''Get seed & features'''
    seed = filtered_df.sample()
    # get seed features
#     year = target['scaled_year'].iat[0]
#     popularity = target['popularity_binned'].iat[0]
    tempo = seed['scaled_tempo'].iat[0]
    loudness = seed['scaled_loudness'].iat[0]
    da = seed['danceability'].iat[0]
    energy = seed['energy'].iat[0]
    return tempo, loudness, da, energy #, popularity


# functionize trainig
def train_knn(filtered_df):
    '''Train knn model'''
    # ready X and y
    features_names = ['scaled_tempo', 'scaled_loudness', 'danceability', 'energy'] # 'scaled_year', 'popularity_binned'
    X = filtered_df[features_names]
    y = filtered_df['track_id']
    # instanciate & train model
    model = KNeighborsRegressor(algorithm='kd_tree', n_jobs=-1).fit(X, y)
    return model


# load trained model
knn_trained = pickle.load(open("peak/knn_trained.pkl","rb")) # in peak/peak


def get_k_dist_ind(knn_trained):
    '''Get model output: distances & indices'''
    # set output & k
    knn_out, k = [], 100
    # get seed features
    tempo, loudness, da, energy = get_seed_features(df)
    # get trained model output for k: distances & indices
    knn_out = knn_trained.kneighbors([[tempo, loudness, da, energy]], n_neighbors=k)
    return knn_out


# get output: distances & indices
knn_out = get_k_dist_ind(knn_trained)
# get indices
ind = knn_out[1][0].tolist()


# recommendations df
rec = df.iloc[ind]







