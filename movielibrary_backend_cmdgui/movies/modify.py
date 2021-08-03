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
    export_data = zip_longest(*list, fillvalue='')
    with open(path+"\\movprimary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("id", "offset"))
        wr.writerows(export_data)
    myfile.close()

#Function for secondary index file i.e movie id and genre
def secindex():
    genre = []
    Primary_key = []
    csv_columns = ["genre", "id"]
    fi_movies= open(path+"\\movies.csv", "r", encoding='utf-8')
    pos = fi_movies.tell()
    line = fi_movies.readline()
    pos = fi_movies.tell()
    line = fi_movies.readline()
    while line:
        line = line.rstrip()
        temp1= line.split(",")
        temp2=temp1[-1].split("|")
        for i in temp2:
            genre.append(i)
            Primary_key.append(temp1[0])
        pos = fi_movies.tell()
        line = fi_movies.readline()
    list = [genre, Primary_key]
    export_data = zip_longest(*list, fillvalue='')
    with open(path+"\\movsecondary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("genre", "id"))
        wr.writerows(export_data)
    myfile.close()

#Function to modify a record first by entering a genre and choosing a primary key from all that have the given genre
def modify():
    id1 = input("Enter genre to modify ")
    dsk_movies = pd.read_csv(path+"\\movsecondary.csv")
    dsk_movies = dsk_movies.loc[dsk_movies['genre'] == id1]
    if id1 in list(dsk_movies['genre']):
        print("Id exists")
        print(dsk_movies)
        while(1):
            id2 = input("enter one of the primary keys from above to modify ")
            if int(id2) in list(dsk_movies['id']):
                break
        dsk_movies = pd.read_csv(path+"\\movsecondary.csv")
        isk =dsk_movies.query('genre == @id1 & id == @id2').index
        dpk_movies = pd.read_csv(path+"\\movprimary.csv")
        ipk = dpk_movies.query('id == @id2').index
        df_movies = pd.read_csv(path+"\\movies.csv")
        iu = df_movies.query('id == @id2').index
        title = input('enter the title:')
        description = input('enter the description:')
        genre = input('enter the genre:')
        df_movies.loc[iu,['title', 'description', 'genre']] =[title, description, genre]
        df_movies.to_csv(path+"\\movies.csv", index=False)
        index()
        secindex()
    else:
        print("Record does not exist")

with open(path+"\\movies.csv", "r") as csvfile:
    choice = int(input('Enter the Choice 1.Modify:\n'))

    if (choice == 1):
        modify()