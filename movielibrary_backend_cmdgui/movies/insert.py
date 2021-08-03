import csv
from itertools import zip_longest
import pandas as pd
import hashlib
import pathlib

path = str(pathlib.Path().absolute())

#Function for the primary index file i.e movie id and offset
def index():
    Offset_address = []
    Primary_key = []
    csv_columns = ["id", "offset"]
    fi_movies = open(path+"\\movies.csv", "r", encoding='utf-8')
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
    with open(path+"\\movprimary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("id", "offset"))
        wr.writerows(export_data)
    myfile.close()

#Function for secondary index file i.e movie id and genre
def secindex():
    genre= []
    Primary_key = []
    csv_columns = ["genre", "id"]
    fi_movies = open(path+"\\movies.csv", "r", encoding='utf-8')
    pos = fi_movies.tell()
    line = fi_movies.readline()
    pos = fi_movies.tell()
    line = fi_movies.readline()
    while line:
        line = line.rstrip()
        temp1 = line.split(",")
        temp2=temp1[-1].split("|")
        for i in temp2:
            genre.append(i)
            Primary_key.append(temp1[0])
        line = fi_movies.readline()
    list = [genre, Primary_key]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted (list, key=lambda x: x[0])
    with open(path+"\\movsecondary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("genre", "id"))
        wr.writerows(export_data)
    myfile.close()

#Function to insert a record in the movie datafile(Must enter id,title,description,genre)
def insert():
    id1 = input("enter the id")
    index()
    secindex()
    dpk_movies = pd.read_csv(path+"\\movprimary.csv", usecols=[0,],header=None)
    
    if id1 in dpk_movies:
        print("id already exists")
    else:
        with open(path+"\\movies.csv", "r", encoding='utf-8') as csvfile:
            title = input('enter the title:')
            description = input('enter the description:')
            genre = input('enter the genre:')
            with open(path+'\\movies.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow('')
                filedname = [id1,title,description,genre]
                print(filedname)
                writer = csv.writer(csvfile, lineterminator='')
                writer.writerow(filedname)
        csvfile.close()
        index()
        secindex()

with open(path+"\\movies.csv", "r") as csvfile:
    choice = int(input('Enter the Choice 1.insert :\n'))

    if (choice == 1):
        insert()
