import csv
from itertools import zip_longest
import pandas as pd
import hashlib

def index():
           Offset_address=[]
           Primary_key=[]
           movieId=[]
           csv_columns=["userId", "movieId", "offset"]
           fi_ratings=open(r"/Users/souravnarayan/Desktop/FS mini/ratings.csv","r",encoding='utf-8')
           pos=fi_ratings.tell()
           line=fi_ratings.readline()
           pos=fi_ratings.tell()
           line=fi_ratings.readline()
           pos = fi_ratings.tell()
           line = fi_ratings.readline()
           while line:
               
               temp=line.split(",")
               #print(a)
               #print(pos,",",a[0],",",a[1])
               Offset_address.append(pos)
               Primary_key.append(temp[0])
               movieId.append(temp[1])
               pos=fi_ratings.tell()
               line=fi_ratings.readline()
           list = [Primary_key, movieId, Offset_address]
           list = zip_longest(*list, fillvalue='')
           export_data = sorted(list, key=lambda x: x[0])
           with open(r'/Users/souravnarayan/Desktop/FS mini/pk3.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
                wr = csv.writer(myfile)
                wr.writerow(("userId", "movieId", "offset"))
                wr.writerows(export_data)
           myfile.close()

def secindex():
    ratings = []
    Primary_key = []
    csv_columns = ["ratings", "id"]
    fsi_ratings = open(r"/Users/souravnarayan/Desktop/FS mini/ratings.csv", "r", encoding='utf-8')
    pos = fsi_ratings.tell()
    line = fsi_ratings.readline()
    #print("Sec")
    pos = fsi_ratings.tell()
    line = fsi_ratings.readline()
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
        pos = fsi_ratings.tell()
        line = fsi_ratings.readline()
    list = [ratings, Primary_key]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted(list, key=lambda x: x[0])
    with open(r"/Users/souravnarayan/Desktop/FS mini/sk3.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("ratings", "id"))
        wr.writerows(export_data)
    myfile.close()

def modify():
    id1 = int(input("Enter id to modify "))
    dsk_ratings = pd.read_csv(r"/Users/souravnarayan/Desktop/FS mini/sk3.csv")
    #print(ds)
    #i = d.iloc[d['name'] == id1]
    #print(i)
    dsk_ratings = dsk_ratings.loc[dsk_ratings['ratings'] == id1]
    #print(list(ds['ratings']))
    if id1 in list(dsk_ratings['ratings']):
        print("Id exists")
        print(dsk_ratings)
        #id2 = ''
        while(1):
            id2 = input("enter one of the primary keys from above to modify ")
            #print(list(ds['id']))
            if id2 in list(dsk_ratings['id']):
                #print(list(ds['id']))
                break
        dsk_ratings = pd.read_csv(r"/Users/souravnarayan/Desktop/FS mini/sk3.csv")
        #i = d.iloc[d['name']==id1 & d['id']==int(id2)]
        #isk = ds.query('ratings == @id1 & id == @id2').index
        #print("i sk" + str(i))
        #ds.to_csv(r"C:\Users\ashok\Desktop\Movie fs\sk.csv", index=False)
        dpk_ratings = pd.read_csv(r"/Users/souravnarayan/Desktop/FS mini/pk3.csv")
        #i = d.index[d['id'] == id2]
        id3=id2.split('|')
        id3 = [int(i) for i in id3]
        #i = dp.query('userId == @id3[0] & movieId == @id3[1]').index
        #print(id3)
        #ipk = dp.query('id == @id2').index
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
        #d = d.drop(i)
        #print(dp)
        #dp.to_csv(r"C:\Users\ashok\Desktop\Movie fs\pk.csv", index=False)
        df_ratings = pd.read_csv(r"/Users/souravnarayan/Desktop/FS mini/ratings.csv")
        iu = df_ratings.query('userId == @id3[0] & movieId == @id3[1]').index
        #print("i user" + str(iu))
        #index()
        #secindex()
        movieId = input('enter the movieId : ')
        ratings = input('enter ratings : ')
        reviews = input('enter the review : ')
        df_ratings.loc[iu,['movieId', 'ratings', 'reviews']] =[movieId, ratings, reviews]
        #print(du)
        #id2 = d['offset']
        #d = d.drop(i)
        #print(d)
        df_ratings.to_csv(r"/Users/souravnarayan/Desktop/FS mini/ratings.csv", index=False)
        index()
        secindex()
        #print(list(d['id']))
        '''imp = open('ratings'.csv', 'rb')
        out = open('ratings.csv', 'wb')
        writer = csv.writer(out)
        for row in csv.reader(imp):
            if row == id1:
                continue
            writer.writerow(row)
        imp.close()
        out.close()
        #print(d)
        #d.loc[d['userId'] == id1]
        #id2 = d['offset']
        #print(id2)
        #new_df = d[~d.id.isin(id1)]
        #new_df.to_csv('pk.csv', index=False, sep=',')'''
        print("Modification Successful ")
    else:
        print("Record does not exist ")
        
def filter():
    id1 = int(input("Enter MovieId "))
    df_ratings = pd.read_csv(r"/Users/souravnarayan/Desktop/FS mini/ratings.csv")
    df_ratings = df_ratings.loc[df_ratings['movieId'] == id1]
    if id1 in list(df_ratings['movieId']):
        print("Id exists")
        df_ratings1 = df_ratings.drop(['movieId'],axis = 1)
        df_user = pd.read_csv(r"/Users/souravnarayan/Desktop/FS mini/user/user.csv")
        id2 = df_ratings1['userId']
        print(id2)
        a = df_user.set_index('userId')['name'].to_dict()
        b = df_ratings1.filter(like='userId')
        df_ratings1[b.columns] = b.replace(a)
        df_ratings1 = df_ratings1.rename(columns={'userId':'username'})
        print(df_ratings1)
        
            


with open(r"/Users/souravnarayan/Desktop/FS mini/ratings.csv", "r") as csvfile:
    # print('successful read')
    choice = int(input('Enter the Choice 1.modify 2.filters :\n'))

    if (choice == 1):
        modify()
    if (choice == 2):
        filter()