
import csv
import hashlib
import pathlib
import pandas as pd
from itertools import zip_longest

path = str(pathlib.Path().absolute())


def mindex():
    Offset_address = []
    Primary_key = []
    csv_columns = ["movieId", "offset"]
    fi_movies = open(path+"\\data\\movies.csv", "r", encoding='utf-8')
    pos = fi_movies.tell()
    line = fi_movies.readline()
    pos = fi_movies.tell()
    line = fi_movies.readline()
    while line:
        temp= line.split(",")
        Offset_address.append(pos)
        Primary_key.append(temp[0])
        pos = fi_movies.tell()
        line = fi_movies.readline()
    list = [ Primary_key, Offset_address]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted(list, key=lambda x: x[0])
    with open(path+"\\data\\\movprimary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("movieId", "offset"))
        wr.writerows(export_data)
    myfile.close()


def rindex():
    Offset_address = []
    Primary_key = []
    movieId = []
    csv_columns = ["userId", "movieId", "offset"]
    fi_ratings = open(path + "\\data\\ratings.csv", "r", encoding='utf-8')
    pos = fi_ratings.tell()
    line = fi_ratings.readline()
    pos = fi_ratings.tell()
    line = fi_ratings.readline()
    while line:
        a = line.split(",")
        # print(a)
        # print(pos,",",a[0],",",a[1])
        Offset_address.append(pos)
        Primary_key.append(a[0])
        movieId.append(a[1])
        pos = fi_ratings.tell()
        line = fi_ratings.readline()
    list = [Primary_key, movieId, Offset_address]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted(list, key=lambda x: x[0])
    with open(path + '\\data\\rprimary.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("userId", "movieId", "offset"))
        wr.writerows(export_data)
    myfile.close()

def uindex():
    Offset_address = []
    Primary_key = []
    csv_columns = ["userId", "offset"]
    fi_user = open(path+"\\data\\user.csv", "r", encoding='utf-8')
    pos = fi_user.tell()
    line = fi_user.readline()
    pos = fi_user.tell()
    line = fi_user.readline()
    while line:
        temp = line.split(",")
        Offset_address.append(pos)
        Primary_key.append(temp[0])
        pos = fi_user.tell()
        line = fi_user.readline()
    list = [ Primary_key, Offset_address]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted(list, key=lambda x: x[0])
    with open(path+"\\data\\uprimary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("userId", "offset"))
        wr.writerows(export_data)
    myfile.close()
