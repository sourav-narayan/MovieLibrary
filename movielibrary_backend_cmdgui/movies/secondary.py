import csv
from itertools import zip_longest
import pandas as pd
import time
import sys
import matplotlib.pyplot as plt


def secindex():
    Offset_address = []
    Primary_key = []
    csv_columns = ["genre", "id"]
    fi = open(r"C:\Users\Nishitha\Documents\movies.csv", "r", encoding='utf-8')
    pos = fi.tell()
    line = fi.readline()
    while line:
        pos = fi.tell()
        line = fi.readline()
        a = line.split(",")
        print(pos, ",", a[-1])
        Offset_address.append(pos)
        Primary_key.append(a[-1])
    list = [Offset_address, Primary_key]
    print(list)
    export_data = zip_longest(*list, fillvalue='')
    with open(r"C:\Users\Nishitha\Documents\movsecondary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("genre", "id"))
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
data = pd.read_csv(r"C:\Users\Nishitha\Documents\movies.csv")
with open(r"C:\Users\Nishitha\Documents\movies.csv") as csvfile:
    # print('successful read')
    choice = int(input('Enter the Choice 1.secondary indexing :\n'))

    if (choice == 1):
        secindex()