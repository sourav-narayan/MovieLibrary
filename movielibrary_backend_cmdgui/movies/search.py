import csv
from itertools import zip_longest
import pandas as pd
import hashlib
import pathlib
import re

path = str(pathlib.Path().absolute())

#Function to search for a 
# def search():
#     id1 = input("Enter movie id ")
#     df_movies = pd.read_csv(path+"\\movies.csv")
#     temp=df_movies[df_movies['id'].str.contains(id1,flags=re.IGNORECASE)]
    
#     print(temp)
def search():
    id1 = int(input("Enter MovieId "))
    df_movies = pd.read_csv(path+"\\movies.csv")
    df_movies = df_movies.loc[df_movies['id'] == id1]
    if id1 in list(df_movies['id']):
        print("Id exists")
        print(df_movies)
    else:
        print("Record does not exist")

choice = int(input("1.Search based on primary key\nEnter your choice\n"))
if choice==1:
    search()


