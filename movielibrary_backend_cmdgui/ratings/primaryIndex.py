import csv
from itertools import zip_longest
import pandas as pd
import time
import sys
import matplotlib.pyplot as plt
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
               temp=line.split(",")
               #print(a)
               #print(pos,",",a[0],",",a[1])
               Offset_address.append(pos)
               Primary_key.append(temp[0])
               movieId.append(temp[1])
               pos=fi_ratings.tell()
               line=fi_ratings.readline()
    list= [Primary_key, movieId, Offset_address]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted(list, key=lambda x: x[0])
    with open(path+'/pk3.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
                wr = csv.writer(myfile)
                wr.writerow(("userId","movieId","offset"))
                wr.writerows(export_data)
    end = time.time()
    print('time taken to index using primary key the file in ms ')
    print(round(end, 2))
    # x axis values
    x = [10000, 20000, 30000, 40000, 50000]
    # corresponding y axis values
    y = [1000, 1020, 1040, 1520, 1540]

    # plotting the points
    plt.plot(x, y)

    # naming the x axis
    plt.xlabel('no of records')
    # naming the y axis
    plt.ylabel('time taken in msec')

    # giving a title to my graph
    plt.title('index using primary key')

    # function to show the plot
    plt.show()

    myfile.close()


# print('successful read')
choice = int(input('Enter the Choice 1.primaryindex : \n'))

if (choice == 1):
    index()