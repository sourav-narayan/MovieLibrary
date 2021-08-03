import csv
import hashlib
import pathlib
import pandas as pd
import re
from itertools import zip_longest
from primary_index import *
from secondary_index import *
from insert import *
from delete import *
from update import *
from movie_display import *
import base64
import io
import numpy as np
import torch
from PIL import Image
from recommendationratings import *
from recommendationtop import *
from recommendationgenre import *

movid = -1
uid = -1
path = str(pathlib.Path().absolute())



def signup():
    id1 = input("enter the id1")
    uindex()
    usecindex()
    dpk_user = pd.read_csv(path+"/data/uprimary.csv", usecols=[0],header=None)
    if id1 in dpk_user.values:
        print("id already exists")
    else:
        with open(path+"/data/user.csv", "r", encoding='utf-8') as csvfile:
            name = input('enter the name :')
            dob = input('enter the dob:')
            gender = input('enter the gender:')
            password = input('enter the password:')
            password = hashlib.md5(password.encode('utf8')).hexdigest()
            with open(
                path+"/data/user.csv", 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow('')
                filedname = [id1, name, dob, gender, password]
                writer = csv.writer(csvfile, lineterminator='')
                writer.writerow(filedname)
        csvfile.close()
        uindex()
        usecindex()
        print("You've been signed up\nPlease login using your credentials")

def login():
    global uid
    global movid
    id = input("Enter user id:")
    df_user = pd.read_csv(path+"/data/user.csv")
    #print(df_user)
    df_user = df_user.loc[df_user['userId'] == int(id)]
    #print(df_user)
    if df_user.empty:
        print("user does not exist")
    else:
        password = input('enter the password:')
        password = hashlib.md5(password.encode('utf8')).hexdigest()
        if str(df_user['password'].values[0]) == password:
            uid = id
            print("Success")
            logged()
        else:
            print("Incorrect password")

def admin():
    id = int(input("Enter admin id:"))
    password = input("Enter admin password:")
    if id == 1234 and password == 'abcd':
        while(1):
            inp = int(input("Please choose the aspect to work on\n1.Movie\n2.Users\n3.Exit\n"))
            if inp == -1:
                break
            elif inp == 1:
                inp = int(input("What would you like to do\n1.Insert Movie record\n2.Modify Existing Movie Record\n3.Delete Existing Movie Record\n4.Back\n"))
                if inp == 1:
                    minsert()
                elif inp == 2 :
                    mupdate()
                elif inp == 3 :
                    mdelete()
                elif inp == 4 :
                    continue
                else:
                    print("Invalid")
            elif inp == 2:
                inp = int(input("What would you like to do\n1.Insert User record\n2.Modify Existing User Record\n3.Delete Existing User Record\n4.Back\n"))
                if inp == 1:
                    uinsert()
                elif inp == 2 :
                    uupdate()
                elif inp == 3 :
                    udelete()
                elif inp == 4 :
                    continue
                else:
                    print("Invalid")
            elif inp == 3:
                break
    else:
        print('Invalid credentials')
def rfilter(id1):
    df_ratings = pd.read_csv(path+"\\data\\ratings.csv")
    df_ratings = df_ratings.loc[df_ratings['movieId'] == id1]
    if id1 in list(df_ratings['movieId']):
        df_ratings1 = df_ratings.drop(['movieId'],axis = 1)
        df_user = pd.read_csv(path+"\\data\\user.csv")
        id2 = df_ratings1['userId']
        a = df_user.set_index('userId')['name'].to_dict()
        b = df_ratings1.filter(like='userId')
        df_ratings1[b.columns] = b.replace(a)
        df_ratings1 = df_ratings1.rename(columns={'userId':'username'})
        print(df_ratings1)

def search_mov(id1):
    global uid
    global movid
    df_movies = pd.read_csv(path+"\\data\\movies.csv")
    df_movies = df_movies.loc[df_movies['movieId'] == id1]
    if id1 in list(df_movies['movieId']):
        while(1):
            display_single(df_movies)
            movid = str(df_movies['movieId'].values[0])
            rfilter(id1)
            print('Recommendation based on title\n')
            display_df(recommendationname(df_movies['title'].values[0]))
            inp = int(input("Enter 1.Enter Rating\n2.Update Rating\n3.Delete Rating\n4.Back\n"))
            if inp == 1:
                rinsert(uid,movid)
            elif inp == 2:
                rupdate(uid,movid)
            elif inp == 3:
                rdelete(uid,movid)
            elif inp == 4:
                movid = -1
                return
            else:
                print('Invalid input')
    else:
        print("Please enter correct movie id")

def logged():
    global uid
    global movid
    while(1):
        inp = int(input("1.Show movies\n2.Select genre\n"))
        if inp == 1:
            print("Trending now:\n")
            display_df(recommendationtop())
            df_movies = pd.read_csv(path + '/data/movies.csv')
            print('All movies:\n')
            display_df(df_movies)
            inp = int(input("Please pick a movie(-1 to logout):"))
            if inp == -1:
                uid = -1
                break
            search_mov(inp)
        elif inp == 2:
            inp1 = input("Enter genre you would like to see:")
            df_movies = pd.read_csv(path + "/data/movies.csv")
            #print(df_movies)
            #print(inp1)
            '''df_movies1 = df_movies.apply(lambda x: pd.Series(x['genre']), axis=1).stack().reset_index(level=1, drop=True)
            df_movies1.name = 'genre'
            gen_md = md.drop('genre', axis=1).join(s)
            print(gen_md)

            df = gen_md[gen_md['genre'].str.contains(genre, flags=re.IGNORECASE)]
            print(df)'''
            df_movies = df_movies[df_movies['genre'].str.contains(inp1,flags=re.IGNORECASE)]
            #print(df_movies)
            display_df(df_movies)
            inp = int(input("Would you like to?\n1.Sort Ascending\n2.Sort Descending\n3.Sort Popularity\n4.Get Recommendation\n5.No\nEnter choice:\n"))#another option popularity
            if inp == 1:
                sorted = df_movies.sort_values('title', ascending=True)
                display_df(sorted)
            elif inp == 2:
                sorted = df_movies.sort_values('title', ascending=False)
                display_df(sorted)
            elif inp == 3:
                display_df(recommendationgenre(inp1,0.1))
            elif inp == 4:
                display_df(recommendationgenre(inp1, 0.85))
            elif inp == 5:
                continue
            inp = int(input("Please pick a movie(-1 to logout):"))
            if inp == -1:
                uid = -1
                break
            search_mov(inp)
        else:
            print('Invalid input')

while(uid == -1):
    inp = int(input("Would you like to :\n1.Login\n2.Signup\n3.Login(Admin)\n4.Exit\n"))
    if inp == 1:
        login()
    elif inp == 2:
        signup()
    elif inp == 3:
        admin()
    elif inp == 4:
        print("Finished")
        break
    else:
        print('invalid input')




