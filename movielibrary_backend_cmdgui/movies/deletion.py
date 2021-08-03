import csv
from itertools import zip_longest
import pandas as pd
import hashlib
import pathlib

path = str(pathlib.Path().absolute())

#Function to delete a record by selecting a genre and then choosing a primary key with the given genre
def delete():
    id1 = input("Enter genre to delete ")
    dsk_movies= pd.read_csv(path+"\\movsecondary.csv")
    dsk_movies = dsk_movies.loc[dsk_movies['genre'] == id1]
    if id1 in list(dsk_movies['genre']):
        print("Id exists")
        print(dsk_movies)
        while(1):
            id2 = int(input("enter one of the primary keys from above to delete "))
            if int(id2) in list(dsk_movies['id']):
                break
        dsk_movies = pd.read_csv(path+"\\movsecondary.csv")
        i=dsk_movies.query('genre == @id1 & id == @id2').index
        dsk_movies = dsk_movies.drop(i)
        dsk_movies.to_csv(path+"\\movsecondary.csv", index=False)
        dpk_movies = pd.read_csv(path+"\\movprimary.csv")
        i = dpk_movies.query('id == @id2').index
        dpk_movies = dpk_movies.drop(i)
        dpk_movies.to_csv(path+"\\movprimary.csv", index=False)
        df_movies = pd.read_csv(path+"\\movies.csv")
        i = df_movies.query('id == @id2').index
        df_movies = df_movies.drop(i)
        df_movies.to_csv(path+"\\movies.csv", index=False)
        print("Record deleted ")
    else:
        print("Record does not exist")

with open(path+"\\movies.csv", "r") as csvfile:
    choice = int(input('Enter the Choice 1.Delete :\n'))

    if (choice == 1):
        delete()