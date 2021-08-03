import csv
from itertools import zip_longest
import pandas as pd
import hashlib
import pathlib
import base64
path = str(pathlib.Path().absolute())

#Function to for formatted display    
def Display():
    df_movies = pd.read_csv(path+"\\movies.csv")
    for index,row in df_movies.iterrows():
        print("Movie id: ",row["movieId"])
        print("Title:  ",row["title"])
        print("Genre:  ",row["genre"]+"\n")
    
choice = int(input('Enter the Choice 1.Display :\n'))
if (choice == 1):
        Display()
