from primary_index import *
from secondary_index import *
import csv
import hashlib
import pathlib
import pandas as pd
from itertools import zip_longest
import base64
import shutil
from PIL import Image

path = str(pathlib.Path().absolute())


def minsert():
    id1 = input("enter the id")
    mindex()
    msecindex()
    dpk_movies = pd.read_csv(path + "\\data\\movprimary.csv", usecols=[0], header=None)
    if id1 in dpk_movies.values:
        print("id already exists")
    else:
        with open(path + "\\data\\movies.csv", "a", encoding='utf-8',newline='') as csvfile:
            title = input('enter the title:')
            description = input('enter the description:')
            genre = input('enter the genre:')
            print("Insert the image")
            imgpath = input("Insert path")
            im = Image.open(imgpath)
            # converting to jpg
            rgb_im = im.convert("RGB")
            # exporting the image
            rgb_im.save(path + "\\data\\images\\" + str(id1) + ".jpg")
            no_of_ratings = average_ratings = 0
            writer = csv.writer(csvfile)
            writer.writerow('')
            filedname = [id1, imgpath, title, description, genre, no_of_ratings, average_ratings]
            print(filedname)
            writer = csv.writer(csvfile, lineterminator='')
            writer.writerow(filedname)
        csvfile.close()
        mindex()
        msecindex()

def rinsert(id1,movieid):
    rindex()
    rsecindex()
    dpk_ratings = pd.read_csv(path+"/data/rprimary.csv", usecols=[0,1],header=None)
    a=list(dpk_ratings.to_records(index=False))
    a1 = 0
    id1, movieid = str(id1), str(movieid)
    x = (id1,movieid)
    #print(x)
    for (index, tuple) in enumerate(a[1:]):
        #print(tuple)
        if tuple[0] == id1 and tuple[1] == movieid:
            a1 = 1
            break
    if (a1):
        print("id already exists")
    else:
        movieid = int(movieid)
        id1 = int(id1)
        with open(path + "/data/ratings.csv", "r", encoding='utf-8') as csvfile:
            ratings = input('give ratings: ')
            reviews = input('enter review: ')
            with open(
                    path + '/data/ratings.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow('')
                filedname = [id1, movieid, ratings, reviews]
                print(filedname)
                writer = csv.writer(csvfile, lineterminator='')
                writer.writerow(filedname)
        csvfile.close()
        df_movies = pd.read_csv(path + "/data/movies.csv" )
        df_movies = df_movies.loc[df_movies['movieId'] == movieid]
        no_of_ratings = int(df_movies['no_of_ratings']) +1
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
        print('done')
        rindex()
        rsecindex()

def uinsert():
    id1 = input("enter the id:")
    uindex()
    usecindex()
    dpk_user = pd.read_csv(path+"\\data\\uprimary.csv", usecols=[0],header=None)
    if id1 in dpk_user.values:
        print("id already exists")
    else:
        with open(path+"\\data\\user.csv", "a", encoding='utf-8',newline='') as csvfile:
            name = input('enter the name :')
            dob = input('enter the dob:')
            gender = input('enter the gender:')
            password = input('enter the password:')
            password = hashlib.md5(password.encode('utf8')).hexdigest()
            writer = csv.writer(csvfile)
            writer.writerow('')
            filedname = [id1, name, dob, gender, password]
            writer = csv.writer(csvfile, lineterminator='')
            writer.writerow(filedname)
        csvfile.close()
        uindex()
        usecindex()
        print("Record Inserted")
