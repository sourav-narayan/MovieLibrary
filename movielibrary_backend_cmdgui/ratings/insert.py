import csv 
from itertools import zip_longest
import pandas as pd
import hashlib
import pathlib

path = str(pathlib.Path().absolute())

def index():
           Offset_address=[]
           Primary_key=[]
           movieId=[]
           csv_columns=["userId", "movieId", "offset"]
           fi_ratings=open(path+"/ratings.csv","r",encoding='utf-8')
           pos=fi_ratings.tell()
           line=fi_ratings.readline()
           pos=fi_ratings.tell()
           line=fi_ratings.readline()
           while line:
               a=line.split(",")
               #print(a)
               #print(pos,",",a[0],",",a[1])
               Offset_address.append(pos)
               Primary_key.append(a[0])
               movieId.append(a[1])
               pos=fi_ratings.tell()
               line=fi_ratings.readline()
           list= [Primary_key, movieId, Offset_address]
           list = zip_longest(*list, fillvalue='')
           export_data = sorted(list, key=lambda x: x[0])
           with open(path+'/pk3.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
                wr = csv.writer(myfile)
                wr.writerow(("userId","movieId","offset"))
                wr.writerows(export_data)
           myfile.close()
    
def secindex():
    ratings = []
    Primary_key = []
    csv_columns = ["ratings", "id"]
    fi_ratings = open(path+"/ratings.csv", "r", encoding='utf-8')
    pos = fi_ratings.tell()
    line = fi_ratings.readline()
    #print("Sec")
    pos = fi_ratings.tell()
    line = fi_ratings.readline()
    while line:
        #pos = fi.tell()
        #line = fi.readline()
        #if line[0] == '\n':
            #break
        line = line.rstrip()
        temp = line.split(",")
        #print(a)
        #print(pos, ",", a[1])
        ratings.append(temp[2])
        Primary_key.append(temp[0]+'|'+temp[1])
        pos = fi_ratings.tell()
        line = fi_ratings.readline()
    list = [ratings, Primary_key]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted(list, key=lambda x: x[0])
    with open(path+"/sk3.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("ratings", "id"))
        wr.writerows(export_data)
    myfile.close()
    
def insert():
    id1 = input("enter the id1 ")
    index()
    secindex()
    dpk_ratings = pd.read_csv(path+"/pk3.csv", usecols=[0,],header=None)
    if id1 in dpk_ratings:
        print("id already exists")
    else:
        with open(path+"/ratings.csv", "r", encoding='utf-8') as csvfile:
            movieid = input('enter the movieId: ')
            ratings = input('give ratings: ')
            reviews = input('enter review: ')
            with open(
                path+'/ratings.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow('')
                filedname = [id1, movieid, ratings, reviews]
                print(filedname)
                writer = csv.writer(csvfile, lineterminator ='')
                writer.writerow(filedname)
        csvfile.close()
        index()
        secindex()




#data = pd.read_csv(r"C:\Users\ashok\Desktop\Movie fs\user.csv")
with open(path+"/ratings.csv", "r") as csvfile:
    # print('successful read')
    choice = int(input('Enter the Choice 1.insert :\n'))

    if (choice == 1):
        insert()


           

