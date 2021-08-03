import csv
from itertools import zip_longest
import pandas as pd
import hashlib
import pathlib

path = str(pathlib.Path().absolute())

def delete():
    id1 = input("Enter id to delete")
    dsk_user = pd.read_csv(path+"\\sk.csv")
    #print(d)
    #i = d.iloc[d['name'] == id1]
    #print(i)
    dsk_user = dsk_user.loc[dsk_user['name'] == id1]
    #print(list(d['name']))
    if id1 in list(dsk_user['name']):
        print("Id exists")
        print(dsk_user)
        #id2 = ''
        while(1):
            id2 = input("enter one of the primary keys from above to delete")
            #print(list(d['id']))
            if int(id2) in list(dsk_user['id']):
                #print(list(d['id']))
                break
        dsk_user = pd.read_csv(path+"\\sk.csv")
        #i = d.iloc[d['name']==id1 & d['id']==int(id2)]
        i=dsk_user.query('name == @id1 & id == @id2').index
        #print("i sk" + str(i))
        dsk_user = dsk_user.drop(i)
        #print(d)
        dsk_user.to_csv(path+"\\sk.csv", index=False)
        dpk_user = pd.read_csv(path+"\\pk.csv")
        #i = d.index[d['id'] == id2]
        i = dpk_user.query('id == @id2').index
        #print("i pk"+str(i))
        #id2 = d.get_value(i, 'offset')
        #id2 = d['offset']
        #print(list(d['id']))
        '''imp = open('pk.csv', 'rb')
        out = open('pk.csv', 'wb')
        writer = csv.writer(out)
        for row in csv.reader(imp):
            if row == id1:
                continue
            writer.writerow(row)
        imp.close()
        out.close()'''
        dpk_user = dpk_user.drop(i)
        #print(d)
        dpk_user.to_csv(path+"\\pk.csv", index=False)
        df_user = pd.read_csv(path+"\\user.csv")
        i = df_user.query('id == @id2').index
        #print("i user" + str(i))
        #id2 = d['offset']
        df_user = df_user.drop(i)
        #print(d)
        df_user.to_csv(path+"\\user.csv", index=False)
        #print(list(d['id']))
        print("Record deleted")
        '''imp = open('user.csv', 'rb')
        out = open('user.csv', 'wb')
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

with open(path+"\\user.csv", "r") as csvfile:
    # print('successful read')
    choice = int(input('Enter the Choice 1.delete :\n'))

    if (choice == 1):
        delete()