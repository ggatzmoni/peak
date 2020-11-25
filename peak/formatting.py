import spotipy
import pandas as pd
import numpy as np
import datetime
import os

def formatting(df):
    df['genres'] = df['genres'].astype(str)
    df['duration_min'] = (df['duration_ms']/60000).astype(int)
    df['decades'] = pd.cut(x=df['year'], bins=[1920, 1930, 1940, 1950,1960,1970,1980,1990,2000,2010,2020])
    df['year'] = df['year'].astype(str)
    return df
