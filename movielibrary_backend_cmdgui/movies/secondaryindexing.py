import csv
from itertools import zip_longest
import pandas as pd
import hashlib
def index():
    Offset_address = []
    Primary_key = []
    csv_columns = ["id", "offset"]
    fi = open(r"C:\Users\Nishitha\Documents\movies.csv", "r", encoding='utf-8')
    pos = fi.tell()
    line = fi.readline()
    while line:
        pos = fi.tell()
        line = fi.readline()
        if line=='\n':
            break
        a = line.split(",")
        print(a)
        print(pos, ",", a[0])
        Offset_address.append(pos)
        Primary_key.append(a[0])
    list = [ Primary_key, Offset_address]
    export_data = zip_longest(*list, fillvalue='')
    with open(r"C:\Users\Nishitha\Documents\movprimary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("id", "offset"))
        wr.writerows(export_data)
    myfile.close()
def secindex():
    name = []
    Primary_key = []
    csv_columns = ["name", "id"]
    fi = open(r"C:\Users\Nishitha\Documents\movies.csv", "r", encoding='utf-8')
    pos = fi.tell()
    line = fi.readline()
    print("Sec")
    while line and line!='\n':
        pos = fi.tell()
        line = fi.readline()
        if line=='\n':
            break
        line = line.rstrip()
        a = line.split(",")
        print(a)
        #print(pos, ",", a[1])
        name.append(a[1])
        Primary_key.append(a[0])
    list = [name, Primary_key]
    print(list)
    export_data = zip_longest(*list, fillvalue='')
    with open(r"C:\Users\Nishitha\Documents\movsecondary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("name", "id"))
        wr.writerows(export_data)
    myfile.close()
def insert():
    id1 = input("enter the id1")
    d = pd.read_csv(r"C:\Users\Nishitha\Documents\movprimary.csv", usecols=[0,],header=None)
    if id1 in d:
        print("id already exists")
    else:
        with open(r"C:\Users\Nishitha\Documents\movies.csv", "r", encoding='utf-8') as csvfile:
            id = input('Enter the id:')
            name = input('enter the name :')
            dob = input('enter the dob:')
            gender = input('enter the gender:')
            password = input('enter the password:')
            password = hashlib.md5(password.encode('utf8')).hexdigest()
            with open(
                r'C:\Users\Nishitha\Documents\movies.csv', 'a', newline='') as csvfile:
                filedname = [id, name, dob, gender, password]
                print(filedname)
                writer = csv.writer(csvfile)
                writer.writerow(filedname)
        csvfile.close()
        index()
        secindex()


data = pd.read_csv(r"C:\Users\Nishitha\Documents\movies.csv")
with open(r"C:\Users\Nishitha\Documents\movies.csv", "r") as csvfile:
    # print('successful read')
    choice = int(input('Enter the Choice 1.insert :\n'))
    if (choice == 1):
        insert()
