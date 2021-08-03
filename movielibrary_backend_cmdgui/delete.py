from primary_index import *
from secondary_index import *
import csv
import hashlib
import pathlib
import pandas as pd
from itertools import zip_longest
import os

path = str(pathlib.Path().absolute())


def mdelete():
    id1 = input("Enter genre to delete ")
    dsk_movies= pd.read_csv(path+"\\data\\movsecondary.csv")
    dsk_movies = dsk_movies.loc[dsk_movies['genre'] == id1]
    if id1 in list(dsk_movies['genre']):
        print("Id exists")
        print(dsk_movies)
        while(1):
            id2 = int(input("enter one of the primary keys from above to delete "))
            if int(id2) in list(dsk_movies['movieId']):
                break
        dsk_movies = pd.read_csv(path+"\\data\\movsecondary.csv")
        i=dsk_movies.query('genre == @id1 & movieId == @id2').index
        dsk_movies = dsk_movies.drop(i)
        dpk_movies = pd.read_csv(path+"\\data\\movprimary.csv")
        i = dpk_movies.query('movieId == @id2').index
        dpk_movies = dpk_movies.drop(i)
        df_movies = pd.read_csv(path+"\\data\\movies.csv")
        i = df_movies.query('movieId == @id2').index
        df_movies = df_movies.drop(i)
        df_movies.to_csv(path+"\\data\\movies.csv", index=False)
        file_data = open(path + "\\data\\movies.csv", 'rb').read()
        open(path + "\\data\\movies.csv", 'wb').write(file_data[:-2])
        os.remove(path+'\\data\\images\\'+str(id2)+'.jpg')
        print("Record deleted ")
        mindex()
        msecindex()
    else:
        print("Record does not exist")


def rdelete(uid,movieid):
    dpk_ratings = pd.read_csv(path + "/data/rprimary.csv", usecols=[0, 1], header=None)
    a = list(dpk_ratings.to_records(index=False))
    a1 = 0
    uid, movieid = str(uid), str(movieid)
    x = (uid, movieid)
    print(x)
    for (index, tuple) in enumerate(a[1:]):
        print(tuple)
        if tuple[0] == uid and tuple[1] == movieid:
            a1 = 1
            break
    if (a1):
        movieid = int(movieid)
        uid = int(uid)
        df_ratings = pd.read_csv(path + "/data/ratings.csv")
        i = df_ratings.query('userId == @uid & movieId == @movieid').index
        df_ratings = df_ratings.drop(i)
        print(df_ratings)
        df_ratings.to_csv(path+"\\data\\ratings.csv", index=False)
        file_data = open(path+"\\data\\ratings.csv", 'rb').read()
        open(path+"\\data\\ratings.csv", 'wb').write(file_data[:-2])
        
        df_movies = pd.read_csv(path + "\\data\\movies.csv" )
        df_movies = df_movies.loc[df_movies['movieId'] == movieid]
        no_of_ratings = int(df_movies['no_of_ratings'].values[0]) -1
        df_movies = pd.read_csv(path + "\\data\\\movies.csv")

        df_ratings = pd.read_csv(path + "\\data\\ratings.csv")
        df_ratings = df_ratings.loc[df_ratings['movieId'] == movieid]
        t = 0
        if movieid in list(df_ratings['movieId']):
            for i in list(df_ratings['ratings']):
                t += i
        if t:
            t /= len(df_ratings.index)
            t = str(round(t,2))
        iu = df_movies.query('movieId == @movieid').index
        df_movies.loc[iu, ['average_ratings','no_of_ratings']] = [t,no_of_ratings]
        df_movies.to_csv(path + "\\data\\movies.csv", index=False)
        rindex()
        rsecindex()
    else:
        print("Record does not exist")

def udelete():
    id1 = input("Enter name to delete")
    dsk_user = pd.read_csv(path+"\\data\\usecondary.csv")
    dsk_user = dsk_user.loc[dsk_user['name'] == id1]
    if id1 in list(dsk_user['name']):
        print("Id exists")
        print(dsk_user)
        while(1):
            id2 = int(input("enter one of the primary keys from above to delete"))
            if id2 in list(dsk_user['userId']):
                break
        dsk_user = pd.read_csv(path+"\\data\\usecondary.csv")
        i=dsk_user.query('name == @id1 & userId == @id2').index
        dsk_user = dsk_user.drop(i)
        dsk_user.to_csv(path+"\\data\\usecondary.csv", index=False)
        dpk_user = pd.read_csv(path+"\\data\\uprimary.csv")
        i = dpk_user.query('userId == @id2').index
        dpk_user = dpk_user.drop(i)
        dpk_user.to_csv(path+"\\data\\uprimary.csv", index=False)
        df_user = pd.read_csv(path+"\\data\\user.csv")
        i = df_user.query('userId == @id2').index
        df_user = df_user.drop(i)
        df_user.to_csv(path+"\\data\\user.csv", index=False)
        file_data = open(path + "\\data\\user.csv", 'rb').read()
        open(path + "\\data\\user.csv", 'wb').write(file_data[:-2])
        print("Record deleted")
        uindex()
        usecindex()
    else:
        print("Record does not exist")
