import csv
from itertools import zip_longest
import pandas as pd
import hashlib


def delete():
    id1 = int(input("Enter ratings to delete "))
    dsk_ratings = pd.read_csv(r"/Users/souravnarayan/Desktop/FS mini/sk3.csv")
    #print(d)
    #i = d.iloc[d['name'] == id1]
    #print(i)
    dsk_ratings = dsk_ratings.loc[dsk_ratings['ratings'] == id1]
    #print(list(d['ratings']))
    if id1 in list(dsk_ratings['ratings']):
        print("id exists")
        print(dsk_ratings)
        #id2 = ''
        while(1):
            id2 = input("enter one of the primary keys from above to delete ")
            #print(list(d['id']))
            if id2 in list(dsk_ratings['id']):
                #print(list(d['id']))
                break
        dsk_ratings = pd.read_csv(r"/Users/souravnarayan/Desktop/FS mini/sk3.csv")
        #i = d.iloc[d['name']==id1 & d['id']==int(id2)]
        i=dsk_ratings.query('ratings == @id1 & id == @id2').index
        print(id1,id2)
        #print("i sk" + str(i))
        dsk_ratings = dsk_ratings.drop(i)
        #print(d)
        dsk_ratings.to_csv(r"/Users/souravnarayan/Desktop/FS mini/sk3.csv", index=False)
        dpk_ratings = pd.read_csv(r"/Users/souravnarayan/Desktop/FS mini/pk3.csv")
        #i = d.index[d['id'] == id2]
        id3=id2.split('|')
        id3 = [int(i) for i in id3]
        i = dpk_ratings.query('userId == @id3[0] & movieId == @id3[1]').index
        #print(id3)
        
        #print("i pk"+str(i))
        #id2 = d.get_value(i, 'offset')
        #id2 = d['offset']
        #print(list(d['id']))
        '''imp = open('pk3.csv', 'rb')
        out = open('pk3.csv', 'wb')
        writer = csv.writer(out)
        for row in csv.reader(imp):
            if row == id1:
                continue
            writer.writerow(row)
        imp.close()
        out.close()'''
        dpk_ratings = dpk_ratings.drop(i)
        #print(d)
        dpk_ratings.to_csv(r"/Users/souravnarayan/Desktop/FS mini/pk3.csv", index=False)
        df_ratings = pd.read_csv(r"/Users/souravnarayan/Desktop/FS mini/ratings.csv")
        i = df_ratings.query('userId == @id3[0] & movieId == @id3[1]').index
        #print("i user" + str(i))
        #id2 = d['offset']
        df_ratings = df_ratings.drop(i)
        #print(d)
        df_ratings.to_csv(r"/Users/souravnarayan/Desktop/FS mini/ratings.csv", index=False)
        #print(list(d['userId']))
        '''imp = open('ratings.csv', 'rb')
        out = open('ratings.csv', 'wb')
        writer = csv.writer(out)
        for row in csv.reader(imp):
            if row == id1:
                continue
            writer.writerow(row)
        imp.close()
        out.close()
        #print(d)
        #d.loc[d['id'] == id1]
        #id2 = d['offset']
        #print(id2)
        #new_df = d[~d.id.isin(id1)]
        #new_df.to_csv('pk.csv', index=False, sep=',')'''
    else:
        print("Record does not exist")

with open(r"/Users/souravnarayan/Desktop/FS mini/ratings.csv", "r") as csvfile:
    # print('successful read')
    choice = int(input('Enter the Choice 1.delete :\n'))

    if (choice == 1):
        delete()