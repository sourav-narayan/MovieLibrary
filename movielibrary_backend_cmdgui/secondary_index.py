import csv
import hashlib
import pathlib
import pandas as pd
from itertools import zip_longest

path = str(pathlib.Path().absolute())


def msecindex():
    genre= []
    Primary_key = []
    csv_columns = ["genre", "movieId"]
    fi_movies = open(path+"\\data\\movies.csv", "r", encoding='utf-8')
    pos = fi_movies.tell()
    line = fi_movies.readline()
    pos = fi_movies.tell()
    line = fi_movies.readline()
    while line:
        line = line.rstrip()
        temp1 = line.split(",")
        temp2=temp1[-3].split("|")
        for i in temp2:
            genre.append(i)
            Primary_key.append(temp1[0])
        line = fi_movies.readline()
    list = [genre, Primary_key]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted (list, key=lambda x: x[0])
    with open(path+"\\data\\movsecondary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("genre", "movieId"))
        wr.writerows(export_data)
    myfile.close()

def rsecindex():
    ratings = []
    Primary_key = []
    csv_columns = ["ratings", "id"]
    fi_ratings = open(path+"\\data\\ratings.csv", "r", encoding='utf-8')
    pos = fi_ratings.tell()
    line = fi_ratings.readline()
    pos = fi_ratings.tell()
    line = fi_ratings.readline()
    while line:
        line = line.rstrip()
        temp = line.split(",")
        ratings.append(temp[2])
        Primary_key.append(temp[0]+'|'+temp[1])
        pos = fi_ratings.tell()
        line = fi_ratings.readline()
    list = [ratings, Primary_key]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted(list, key=lambda x: x[0])
    with open(path+"\\data\\rsecondary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("ratings", "id"))
        wr.writerows(export_data)
    myfile.close()

def usecindex():
    name = []
    Primary_key = []
    csv_columns = ["name", "userId"]
    fi_user = open(path+"\\data\\user.csv", "r", encoding='utf-8')
    pos = fi_user.tell()
    line = fi_user.readline()
    pos = fi_user.tell()
    line = fi_user.readline()
    while line:
        line = line.rstrip()
        temp = line.split(",")
        name.append(temp[1])
        Primary_key.append(temp[0])
        pos = fi_user.tell()
        line = fi_user.readline()
    list = [name, Primary_key]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted(list, key=lambda x: x[0])
    with open(path+"\\data\\usecondary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("name", "userId"))
        wr.writerows(export_data)
    myfile.close()

