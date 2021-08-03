import csv
from itertools import zip_longest
import pandas as pd
import time
import sys
import matplotlib.pyplot as plt
import pathlib

path = str(pathlib.Path().absolute())


def secindex():
    Offset_address = []
    Primary_key = []
    csv_columns = ["ratings", "userId"]
    fi_ratings = open(path+"/ratings.csv", "r", encoding='utf-8')
    pos = fi_ratings.tell()
    line = fi_ratings.readline()
    while line:
        pos = fi_ratings.tell()
        line = fi_ratings.readline()
        temp = line.split(",")
        #print(pos, ",", a[-1])
        Offset_address.append(pos)
        Primary_key.append(temp[-1])
    list = [Offset_address, Primary_key]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted(list, key=lambda x: x[0])
    with open(path+"/sk3.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("ratings", "userId"))
        wr.writerows(export_data)
        end = time.time()
        print('time taken to index the file in ms')
        print(round(end, 2))
        # x axis values
        x = [10000, 20000, 30000, 40000, 50000]
        # corresponding y axis values
        y = [1000, 1420, 1460, 1520, 1540]

        # plotting the points
        plt.plot(x, y)

        # naming the x axis
        plt.xlabel('no of records')
        # naming the y axis
        plt.ylabel('time taken in msec')

        # giving a title to my graph
        plt.title('index using secondary key')

        # function to show the plot
        plt.show()
    myfile.close()


start = time.time()
data = pd.read_csv(path+"/ratings.csv")
with open(path+"/ratings.csv") as csvfile:
    # print('successful read')
    choice = int(input('Enter the Choice 1.secondary indexing :\n'))

    if (choice == 1):
        secindex()