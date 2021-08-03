import pandas as pd
import pathlib
import base64
import io
from PIL import Image

path = str(pathlib.Path().absolute())


# Function to for formatted display
def display_single(df_movies):
    print("Movie id: ", df_movies["movieId"].values[0])
    print("Title:  ", df_movies["title"].values[0])
    print("Description:  ",df_movies["description"].values[0])
    print("Genre:  ",df_movies["genre"].values[0] + "\n")
    #print(path+df_movies['img'])
    img = Image.open(path+df_movies['img'].values[0])
    img.show()


def display_df(df_movies):
    for index,row in df_movies.iterrows():
        print("Movie id: ",row["movieId"])
        '''
        imgdata = base64.b64decode(row['img'])
        im_file = io.BytesIO(imgdata) 
        img = Image.open(im_file)
        img.show(img)
    '''
        print("Title:  ",row["title"])
        print("Genre:  ",row["genre"]+"\n")
