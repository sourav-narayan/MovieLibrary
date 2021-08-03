import csv
from itertools import zip_longest
import pandas as pd
import hashlib
import pathlib

path = str(pathlib.Path().absolute())
def index():
    Offset_address = []
    Primary_key = []
    csv_columns = ["id", "offset"]
    fi_user = open(path+"\\user.csv", "r", encoding='utf-8')
    pos = fi_user.tell()
    line = fi_user.readline()
    pos = fi_user.tell()
    line = fi_user.readline()
    while line:
        #if line[0]=='\n':
            #break
        temp = line.split(",")
        #print(a)
        #print(pos, ",", a[0])
        Offset_address.append(pos)
        Primary_key.append(temp[0])
        pos = fi_user.tell()
        line = fi_user.readline()
    list = [ Primary_key, Offset_address]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted(list, key=lambda x: x[0])
    with open(path+"\\pk.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("id", "offset"))
        wr.writerows(export_data)
    myfile.close()

def secindex():
    name = []
    Primary_key = []
    csv_columns = ["name", "id"]
    fi_user = open(path+"\\user.csv", "r", encoding='utf-8')
    pos = fi_user.tell()
    line = fi_user.readline()
    #print("Sec")
    pos = fi_user.tell()
    line = fi_user.readline()
    while line:
        #pos = fi.tell()
        #line = fi.readline()
        #if line[0] == '\n':
            #break
        line = line.rstrip()
        temp = line.split(",")
        #print(a)
        #print(pos, ",", a[1])
        name.append(temp[1])
        Primary_key.append(temp[0])
        pos = fi_user.tell()
        line = fi_user.readline()
    list = [name, Primary_key]
    list = zip_longest(*list, fillvalue='')
    export_data = sorted(list, key=lambda x: x[0])
    with open(path+"\\sk.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("name", "id"))
        wr.writerows(export_data)
    myfile.close()

def modify():
    id1 = input("Enter id to delete")
    dsk_user = pd.read_csv(path+"\\sk.csv")
    #print(ds)
    #i = d.iloc[d['name'] == id1]
    #print(i)
    dsk_user = dsk_user.loc[dsk_user['name'] == id1]
    #print(list(ds['name']))
    if id1 in list(dsk_user['name']):
        print("Id exists")
        #print(ds)
        #id2 = ''
        while(1):
            id2 = input("enter one of the primary keys from above to modify")
            print(list(dsk_user['id']))
            if int(id2) in list(dsk_user['id']):
                print(list(dsk_user['id']))
                break
        dsk_user = pd.read_csv(path+"\\sk.csv")
        #i = d.iloc[d['name']==id1 & d['id']==int(id2)]
        isk =dsk_user.query('name == @id1 & id == @id2').index
        #print("i sk" + str(i))
        #ds.to_csv(r"C:\Users\ashok\Desktop\Movie fs\sk.csv", index=False)
        dpk_user = pd.read_csv(path+"\\pk.csv")
        #i = d.index[d['id'] == id2]
        ipk = dpk_user.query('id == @id2').index
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
        #d = d.drop(i)
        #print(dp)
        #dp.to_csv(r"C:\Users\ashok\Desktop\Movie fs\pk.csv", index=False)
        df_user = pd.read_csv(path+"\\user.csv")
        iu = df_user.query('id == @id2').index
        #print("i user" + str(iu))
        #index()
        #secindex()
        name = input('enter the name :')
        dob = input('enter the dob:')
        gender = input('enter the gender:')
        password = input('enter the password:')
        password = hashlib.md5(password.encode('utf8')).hexdigest()
        df_user.loc[iu,['name', 'dob', 'gender', 'password']] =[name, dob, gender, password]
        index()
        secindex()
        #id2 = d['offset']
        #d = d.drop(i)
        #print(d)
        df_user.to_csv(path+"\\user.csv", index=False)
        print("Record modified")
        #print(list(d['id']))
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
    choice = int(input('Enter the Choice 1.modify :\n'))

    if (choice == 1):
        modify()