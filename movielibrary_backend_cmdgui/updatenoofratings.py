import csv
import hashlib
import pathlib
import re

import pandas as pd
from itertools import zip_longest
from primary_index import *
from secondary_index import *
from insert import *
from delete import *
from update import *

import base64
import io
import numpy as np
import torch
from PIL import Image
import os

uid = -1
path = str(pathlib.Path().absolute())

def rupdate():
    rindex()
    rsecindex()
    dpk_ratings = pd.read_csv(path+"\\data\\ratings.csv")

    t = [[0] * 2 for i in range(131)]
    l = 0
    for i in list(dpk_ratings['movieId']):
        t[i][0] += 1
        t[i][1] += (dpk_ratings._get_value(l, 'ratings'))
        l += 1
    for i in range(100, 121):
        if t[i][0]:
            t[i][1] /= t[i][0]
    for i in range(100, 121):
        print(type(t[i][1]))
        t[i][1] = str(round(t[i][1], 2))

    print(t)
    df_movies = pd.read_csv(path + "\\data\\movies.csv")
    for i in range(100, 121):
        iu = df_movies.query('movieId == @i').index
        df_movies.loc[iu, ['average_ratings','no_of_ratings']] = [t[i][1],t[i][0]]
    df_movies.to_csv(path + "\\data\\movies.csv", index=False)

def filter():
    id1 = int(input("Enter MovieId "))
    df_ratings = pd.read_csv(path + "\\data\\ratings.csv")
    df_ratings = df_ratings.loc[df_ratings['movieId'] == id1]
    t = [0]
    if id1 in list(df_ratings['movieId']):
        for index,row in df_ratings.iterrows():
            print( row["ratings"])
    print(df_ratings)
    print(len(df_ratings.index))


def ainsert():
    id1 = input("enter the id1 ")
    movieid = input('enter the movieId: ')
    rindex()
    rsecindex()
    dpk_ratings = pd.read_csv(path+"/data/rprimary.csv", usecols=[0,1],header=None)
    a=list(dpk_ratings.to_records(index=False))
    a1=0
    x = (id1,movieid)
    print(a,x)
    for (index, tuple) in enumerate(a[1:]):
        print(tuple[0] == id1,tuple[1] == movieid)
        if tuple[0] == id1 and tuple[1] == movieid:
            a1 = tuple
            print(a1)
            break
    print(a1)
    if (a1):
        print("id already exists")
    else:
        print('doest')


def imginsert():
    id1 = input("Insert path")
    id2 = input ("Input movie id")
    file = open(id1, 'rb')
    im_b64 = base64.b64encode(file.read())
    file.close()
    df_movies = pd.read_csv(path + "\\data\\movies.csv")
    imgdata = base64.b64decode(im_b64)
    im_file = io.BytesIO(imgdata)  # convert image to file-like object
    img = Image.open(im_file)
    img.show(img)

def iminsert():
    df_movies = pd.read_csv(path + "\\data\\movies.csv")
    for i in range(100, 121):
        img_path = path+'\\images\\'+str(i)+'.jpeg'
        #im_file = io.BytesIO(imgdata)  # convert image to file-like object
        #img = Image.open(im_file)
        #img.show(img)
        im = Image.open(img_path)
        # converting to jpg
        rgb_im = im.convert("RGB")
        # exporting the image
        rgb_im.save(path+"\\data\\images\\" + str(i) + ".jpg")

def display_df(df_movies):
    for index,row in df_movies.iterrows():
        print("Movie id: ",row["movieId"])
        '''
        imgdata = base64.b64decode(row['img'])
        im_file = io.BytesIO(imgdata) 
        img = Image.open(im_file)
        img.show(img)
    '''
        print("Title:  ",row["title"])
        print("Genre:  ",row["genre"]+"\n")
df_movies = pd.read_csv(path + "\\data\\movies.csv")


def get_genre():
    mindex()
    msecindex()
    df_movies = pd.read_csv(path + "\\data\\movsecondary.csv")
    df = df_movies['genre'].drop_duplicates().to_list()
    print(df)
    res = [i for i in df if i.lower().startswith('com')]
    print(res)
    '''df_list = [df_list.append((i.split('|')) for i in df]
    print(df_list)
    flat_list = [item for sublist in df_list for item in sublist]
    print(flat_list)'''

