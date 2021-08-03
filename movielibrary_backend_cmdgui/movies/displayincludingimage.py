import csv
from itertools import zip_longest
import pandas as pd
import hashlib
import pathlib
import base64
path = str(pathlib.Path().absolute())

#Function to for formatted display    
def Display():
    df_movies = pd.read_csv(path+"\\movies.csv")
    for index,row in df_movies.iterrows():
        print("Movie id:",end=" ")
        print(row["d"])
        print("Title:",end=" ")
        print(row["title"])
        print("Description:",end=" ")
        print(row["description"])
        print("Genre:",end=" ")
        print(row["genre"]+"\n")
        # id1 = input("Insert path")
        # id2 = input ("Input movie id")
        file = open(imgpath, 'rb')
        im_b64 = base64.b64encode(file.read())
        # file.close()
        df_movies = pd.read_csv(path + "\\movies.csv")
        imgdata = base64.b64decode(im_b64)
        im_file = io.BytesIO(imgdata)  # convert image to file-like object
        img = Image.open(im_file)
        img.show(img)
    
choice = int(input('Enter the Choice 1.Display :\n'))
if (choice == 1):
        Display()
