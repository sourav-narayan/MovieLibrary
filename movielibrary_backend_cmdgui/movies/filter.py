import csv
from itertools import zip_longest
import pandas as pd
import hashlib
import pathlib
import re

path = str(pathlib.Path().absolute())

#Function to filter the movies based on genre and then sort the movies in descending order based on title
def displaydesc():
    id1 = input("Enter genre ")
    df_movies = pd.read_csv(path+"\\movies.csv")
    df_movies=df_movies[df_movies['genre'].str.contains(id1,flags=re.IGNORECASE)]
    sorted = df_movies.sort_values('title', ascending=False)
    print(sorted)

#Function to filter the movies based on genre and then sort the movies in asscending order based on title
def displayasc():
     id1 = input("Enter genre ")
     df_movies = pd.read_csv(path+"\\movies.csv")
     df_movies=df_movies[df_movies['genre'].str.contains(id1,flags=re.IGNORECASE)]
     sorted = df_movies.sort_values('title', ascending=True)
     print(sorted)

#Function to filter the movies based on genre and then display movies without sorting
def display():
     id1 = input("Enter genre ")
     df_movies = pd.read_csv(path+"\\movies.csv")
     df_movies=df_movies[df_movies['genre'].str.contains(id1,flags=re.IGNORECASE)]
     sorted = df_movies.sort_values('title')
     print(sorted)

choice = int(input("1.Ascending order\n2.Descending Order\n3.No Sort\nEnter your choice"))
if choice==1:
    displayasc()
elif choice==2:
    displaydesc()
else:
    display()

