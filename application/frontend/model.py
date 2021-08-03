import csv
import glob
import hashlib
import os
import pathlib
import re
from itertools import zip_longest
from PIL import Image
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from datetime import datetime

from frontend.app import app, login_manager
#from util.records import get_new_rec_offset, write_into_files, write_game_count, get_game_count
from flask_login import UserMixin

path = str(pathlib.Path().absolute())

@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)


class Movie:
    mode = 1
    count = 0

    def __init__(self, movieId, title, imgpath, genre, desc, avg_ratings):
        self.movieId = movieId
        self.title = title
        self.imgpath = imgpath
        self.genre = genre
        self.description = desc
        self.avg_ratings = avg_ratings

    '''def __str__(self):
        return "\nName : "+self.name+"\nGenre : "+self.genre+"\nPlatforms supported : "+self.pf+"\nDescription : "\
               + self.desc + "\nPublisher : " + self.pub + \
            "\nRelease Date : "+self.r_date+"\nPrice : "+self.price'''

    #Check if the movie exists based on movieId or title
    @staticmethod
    def check_movieId(movieId = False):
        if movieId:
            movieId = int(movieId)
            df_movies = pd.read_csv(path + "/data/movies.csv")
            df_movies = df_movies.loc[df_movies['movieId'] == movieId]
            if movieId in list(df_movies['movieId']):
                return True
            else:
                return False


    #check if genre exists
    @staticmethod
    def get_genre():
        Movie.mindex()
        Movie.msecindex()
        df_movies = pd.read_csv(path + "/data/movsecondary.csv")
        df_movies = df_movies['genre'].drop_duplicates().to_list()
        return df_movies

    #Retieve list of movieId for given genre
    @staticmethod
    def find_genre_search(genre, sortkey):
        Movie.mindex()
        Movie.msecindex()
        sortkey = int(sortkey)
        df_movies = pd.read_csv(path + "/data/movies.csv")
        df_movies = df_movies.loc[df_movies['genre'].str.contains(genre, flags=re.IGNORECASE)]
        mov_obj = []
        if df_movies.empty:
            print("Record does not exist")
            return mov_obj
        else:
            print("Id exists")
            if sortkey == 1:
                df_movies = df_movies.sort_values('title', ascending=True)
            elif sortkey == 2:
                df_movies = df_movies.sort_values('title', ascending=False)
            elif sortkey == 3:
                genre_list = Movie.get_genre()
                res = [i for i in genre_list if i.lower().startswith(genre.lower())][0]
                df_movies = Movie.recommendationgenre(genre=res, percentile=0)
            for index, row in df_movies.iterrows():
                mov_obj.append(Movie(row['movieId'], row['title'],
                                     row['img'], row['genre'],
                                     row['description'], row['average_ratings']))
            return mov_obj

    @staticmethod
    def find_genre(genre):
        Movie.mindex()
        Movie.msecindex()
        dsk_movies = pd.read_csv(path + "/data/movies.csv")
        dsk_movies = dsk_movies.loc[dsk_movies['genre'].str.contains(genre, flags=re.IGNORECASE)]
        mov_obj = []
        if dsk_movies.empty:
            print("Record does not exist")
            return mov_obj
        else:
            print("Id exists")
            for index, row in dsk_movies.iterrows():
                mov_obj.append(Movie(movieId=row['movieId'], title='', imgpath='', genre='', desc='', avg_ratings=''))
            return mov_obj

    @staticmethod
    def get_all_movies():
        df_movies = pd.read_csv(path + '/data/movies.csv')
        mov_obj = []
        for index, row in df_movies.iterrows():
            mov_obj.append(Movie(row['movieId'], row['title'],
                                 row['img'], row['genre'],
                                 row['description'], row['average_ratings']))
        return mov_obj

    #Retrieve single movie data based on movieId or title
    @staticmethod
    def search(movieId = False, title = False):
        mov_obj = []
        if movieId:
            movieId = int(movieId)
            df_movies = pd.read_csv(path + "/data/movies.csv")
            df_movies = df_movies.loc[df_movies['movieId'] == movieId]
            if movieId in list(df_movies['movieId']):
                mov_obj = Movie(df_movies['movieId'].values[0], df_movies['title'].values[0],
                                df_movies['img'].values[0], df_movies['genre'].values[0],
                                df_movies['description'].values[0], df_movies['average_ratings'].values[0])
                return mov_obj
            else:
                print('MovieId incorrect')
                return mov_obj
        elif title:
            df_movies = pd.read_csv(path + "/data/movies.csv")
            df_movies = df_movies.loc[df_movies['title'].str.contains(title, flags=re.IGNORECASE)]
            if df_movies.empty:
                print('Movie title incorrect')
                return mov_obj
            else:
                for index, row in df_movies.iterrows():
                    mov_obj.append(Movie(row['movieId'], row['title'],
                                         row['img'], row['genre'],
                                         row['description'], row['average_ratings']))
                return mov_obj
        else:
            print("Please enter MovieId or title")
            return mov_obj

    #Get trending recommendations based on genre
    @staticmethod
    def recommendationgenre(genre, percentile=0.85):
        # df = gen_md[gen_md['genre'] == genre]
        features = 'genre'
        md = pd.read_csv(path + '/data/movies.csv')
        if genre in list(md['genre']):
            s = md.apply(lambda x: pd.Series(x['genre']), axis=1).stack().reset_index(level=1, drop=True)
            s.name = 'genre'
            gen_md = md.drop('genre', axis=1).join(s)
            # print(gen_md)

            df = gen_md[gen_md['genre'].str.contains(genre, flags=re.IGNORECASE)]
            # print(df)
            C = df['average_ratings'].mean()
            m = df['no_of_ratings'].quantile(percentile)
            # print(vote_counts.values,vote_averages.values)

            qualified = \
                df[(df['no_of_ratings'] >= m) & (df['no_of_ratings'].notnull()) & (df['average_ratings'].notnull())][
                    ['movieId', 'img', 'title', 'genre', 'description', 'no_of_ratings', 'average_ratings']]
            qualified['no_of_ratings'] = qualified['no_of_ratings'].astype('int')
            qualified['average_ratings'] = qualified['average_ratings'].astype('int')

            qualified['wr'] = qualified.apply(
                lambda x: (x['no_of_ratings'] / (x['no_of_ratings'] + m) * x['average_ratings']) + (
                        m / (m + x['no_of_ratings']) * C), axis=1)
            qualified = qualified.sort_values('wr', ascending=False)
            return qualified

    #Get Top Trending recommendation
    @staticmethod
    def recommendationtop():
        df2 = pd.read_csv(path + '/data/movies.csv')
        # print(df2)
        C = df2['average_ratings'].mean()
        m = df2['no_of_ratings'].quantile(0.9)
        q_movies = df2.copy().loc[df2['no_of_ratings'] >= m]
        q_movies.shape

        # print(q_movies.shape)

        def weighted_rating(x, m=m, C=C):
            v = x['no_of_ratings']
            R = x['average_ratings']
            # Calculation based on the IMDB formula
            return (v / (v + m) * R) + (m / (m + v) * C)

        q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
        qualifiedtop = q_movies.sort_values('score', ascending=False).head(5)

        mov_obj = []
        for index, row in qualifiedtop.iterrows():
            mov_obj.append(Movie(row['movieId'], row['title'],
                                 row['img'], row['genre'],
                                 row['description'], row['average_ratings']))
        return mov_obj

    #Get recommendation based on similar movies (rating based)
    @staticmethod
    def recommendationname(movie_name):
        movies = pd.read_csv(path + '/data/movies.csv')
        ratings = pd.read_csv(path + '/data/ratings.csv')
        if movie_name in list(movies['title']):
            final_dataset = ratings.pivot(index='movieId', columns='userId', values='ratings')
            final_dataset.fillna(0, inplace=True)

            csr_data = csr_matrix(final_dataset.values)

            final_dataset.reset_index(inplace=True)
            knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
            knn.fit(csr_data)

            n_movies_to_reccomend = 10
            movie_list = movies[movies['title'].str.contains(movie_name)]
            if len(movie_list):
                movie_idx = movie_list.iloc[0]['movieId']
                movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
                distances, indices = knn.kneighbors(csr_data[movie_idx], n_neighbors=n_movies_to_reccomend + 1)
                rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
                                           key=lambda x: x[1])[:0:-1]
                recommend_frame = []
                for val in rec_movie_indices:
                    movie_idx = final_dataset.iloc[val[0]]['movieId']
                    idx = movies[movies['movieId'] == movie_idx].index
                    recommend_frame.append(
                        {'movieId': movies.iloc[idx]['movieId'].values[0], 'img': movies.iloc[idx]['img'].values[0],
                         'title': movies.iloc[idx]['title'].values[0], 'genre': movies.iloc[idx]['genre'].values[0],
                         'description': movies.iloc[idx]['description'].values[0],
                         'average_ratings': movies.iloc[idx]['average_ratings'].values[0],'distance': val[1]})
                qualified = pd.DataFrame(recommend_frame, index=range(1, n_movies_to_reccomend + 1)).head(4)
                mov_obj = []
                for index, row in qualified.iterrows():
                    mov_obj.append(Movie(row['movieId'], row['title'],
                                         row['img'], row['genre'],
                                         row['description'], row['average_ratings']))
                return mov_obj

    @staticmethod
    def mindex():
        Offset_address = []
        Primary_key = []
        csv_columns = ["movieId", "offset"]
        fi_movies = open(path + "/data/movies.csv", "r", encoding='utf-8')
        pos = fi_movies.tell()
        line = fi_movies.readline()
        pos = fi_movies.tell()
        line = fi_movies.readline()
        while line:
            temp = line.split(",")
            Offset_address.append(pos)
            Primary_key.append(temp[0])
            pos = fi_movies.tell()
            line = fi_movies.readline()
        list = [Primary_key, Offset_address]
        list = zip_longest(*list, fillvalue='')
        export_data = sorted(list, key=lambda x: x[0])
        with open(path + "/data/movprimary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(("movieId", "offset"))
            wr.writerows(export_data)
        myfile.close()

    @staticmethod
    def msecindex():
        genre = []
        Primary_key = []
        csv_columns = ["genre", "movieId"]
        fi_movies = open(path + "/data/movies.csv", "r", encoding='utf-8')
        pos = fi_movies.tell()
        line = fi_movies.readline()
        pos = fi_movies.tell()
        line = fi_movies.readline()
        while line:
            line = line.rstrip()
            temp1 = line.split(",")
            temp2 = temp1[-3].split("|")
            for i in temp2:
                genre.append(i)
                Primary_key.append(temp1[0])
            line = fi_movies.readline()
        list = [genre, Primary_key]
        list = zip_longest(*list, fillvalue='')
        export_data = sorted(list, key=lambda x: x[0])
        with open(path + "/data/movsecondary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(("genre", "movieId"))
            wr.writerows(export_data)
        myfile.close()

    @staticmethod
    def minsert(id1, title, imgpath, description,genre):
        id1 = int(id1)
        Movie.mindex()
        Movie.msecindex()
        dpk_movies = pd.read_csv(path + "/data/movprimary.csv", usecols=[0], header=None)
        with open(path + "/data/movies.csv", "a", encoding='utf-8', newline='') as csvfile:
            no_of_ratings = average_ratings = 0
            writer = csv.writer(csvfile)
            writer.writerow('')
            filedname = [id1, '/frontend/static/images/'+str(id1)+'.jpg', title, description, genre, no_of_ratings, average_ratings]
            print(filedname)
            writer = csv.writer(csvfile, lineterminator='')
            writer.writerow(filedname)
        csvfile.close()
        Movie.mindex()
        Movie.msecindex()

    @staticmethod
    def mupdate(id1, title, imgpath, description,genre):
            dsk_movies = pd.read_csv(path + "/data/movsecondary.csv")
            isk = dsk_movies.query('genre == @genre & movieId == @id1').index
            dpk_movies = pd.read_csv(path + "/data/movsecondary.csv")
            ipk = dpk_movies.query('movieId == @id1').index
            df_movies = pd.read_csv(path + "/data/movies.csv")
            iu = df_movies.query('movieId == @id1').index
            df_movies.loc[iu, ['title', 'description', 'genre']] = [title, description, genre]
            df_movies.to_csv(path + "/data/movies.csv", index=False)
            Movie.mindex()
            Movie.msecindex()

    @staticmethod
    def mdelete(genre, movieId):
        df_movies = pd.read_csv(path + "/data/movies.csv")
        i = df_movies.query('movieId == @movieId').index
        df_movies = df_movies.drop(i)
        df_movies.to_csv(path + "/data/movies.csv", index=False)
        file_data = open(path + "/data/movies.csv", 'rb').read()
        open(path + "/data/movies.csv", 'wb').write(file_data[:-2])
        print("Record deleted ")
        Movie.mindex()
        Movie.msecindex()


class Users(UserMixin):

    def __init__(self, userId, username, password):
        self.id = userId
        self.username = username
        self.password = password

    #check if user exists
    @staticmethod
    def check_userId(userId):
        Users.uindex()
        Users.usecindex()
        userId = int(userId)
        df_user = pd.read_csv(path + "/data/uprimary.csv")
        df_user = df_user.loc[df_user['userId'] == userId]
        if df_user.empty:
            return False
        return True

    ''''#Check if password is correct
    @staticmethod
    def check_password(user_id, password):
        print(user_id)
        #userId = int(user_id)
        df_user = pd.read_csv(path + "/data/user.csv")
        df_user = df_user.loc[df_user['userId'] == user_id]
        if df_user.empty:
            return False
        else:
            password = hashlib.md5(password.encode('utf8')).hexdigest()
            if str(df_user['password'].values[0]) == password:
                return True
            else:
                return False'''

    #Get the user data
    @staticmethod
    def get(user_id):
        Users.uindex()
        Users.usecindex()
        user_id = int(user_id)
        df_user = pd.read_csv(path + "/data/user.csv")
        df_user = df_user.loc[df_user['userId'] == user_id]
        if df_user.empty:
            return None
        else:
            return Users(df_user['userId'].values[0], df_user['name'].values[0], df_user['password'].values[0])

    #Get list of userId for username
    @staticmethod
    def ufind(uname):
        Users.uindex()
        Users.usecindex()
        dsk_users = pd.read_csv(path + "/data/usecondary.csv")
        dsk_users = dsk_users.loc[dsk_users['name'].str.contains(uname, flags=re.IGNORECASE)]
        user_obj = []
        if dsk_users.empty:
            print("Record does not exist")
            return user_obj
        else:
            print("Id exists")
            for index, row in dsk_users.iterrows():
                user_obj.append(Users(userId=row['userId'],username='',password=''))
            return user_obj


    @staticmethod
    def uindex():
        Offset_address = []
        Primary_key = []
        csv_columns = ["userId", "offset"]
        fi_user = open(path + "/data/user.csv", "r", encoding='utf-8')
        pos = fi_user.tell()
        line = fi_user.readline()
        pos = fi_user.tell()
        line = fi_user.readline()
        while line:
            temp = line.split(",")
            Offset_address.append(pos)
            Primary_key.append(temp[0])
            pos = fi_user.tell()
            line = fi_user.readline()
        list = [Primary_key, Offset_address]
        list = zip_longest(*list, fillvalue='')
        export_data = sorted(list, key=lambda x: x[0])
        with open(path + "/data/uprimary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(("userId", "offset"))
            wr.writerows(export_data)
        myfile.close()

    @staticmethod
    def usecindex():
        name = []
        Primary_key = []
        csv_columns = ["name", "userId"]
        fi_user = open(path + "/data/user.csv", "r", encoding='utf-8')
        pos = fi_user.tell()
        line = fi_user.readline()
        pos = fi_user.tell()
        line = fi_user.readline()
        while line:
            line = line.rstrip()
            temp = line.split(",")
            name.append(temp[1])
            Primary_key.append(temp[0])
            pos = fi_user.tell()
            line = fi_user.readline()
        list = [name, Primary_key]
        list = zip_longest(*list, fillvalue='')
        export_data = sorted(list, key=lambda x: x[0])
        with open(path + "/data/usecondary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(("name", "userId"))
            wr.writerows(export_data)
        myfile.close()


    @staticmethod
    def uinsert(id1, name, dob, gender, password):
        Users.uindex()
        Users.usecindex()
        dob = dob.strftime("%m-%d-%Y")
        with open(path + "/data/user.csv", "a", encoding='utf-8', newline='') as csvfile:
            password = hashlib.md5(password.encode('utf8')).hexdigest()
            writer = csv.writer(csvfile)
            writer.writerow('')
            filedname = [id1, name, dob, gender, password]
            writer = csv.writer(csvfile, lineterminator='')
            writer.writerow(filedname)
        csvfile.close()
        Users.uindex()
        Users.usecindex()
        print("Record Inserted")

    @staticmethod
    def udelete(name, userId):
        userId = int(userId)
        df_user = pd.read_csv(path + "/data/user.csv")
        i = df_user.query('userId == @userId').index
        df_user = df_user.drop(i)
        df_user.to_csv(path + "/data/user.csv", index=False)
        file_data = open(path + "/data/user.csv", 'rb').read()
        open(path + "/data/user.csv", 'wb').write(file_data[:-2])
        print("Record deleted")
        Users.uindex()
        Users.usecindex()
        print('User Deleted')

    @staticmethod
    def uupdate(name, userId, name1, dob, gender, password):
        df_user = pd.read_csv(path + "/data/user.csv")
        dob = dob.strftime("%m-%d-%Y")
        iu = df_user.query('userId == @userId').index
        password = hashlib.md5(password.encode('utf8')).hexdigest()
        df_user.loc[iu, ['name', 'dob', 'gender', 'password']] = [name1, dob, gender, password]
        df_user.to_csv(path + "/data/user.csv", index=False)
        Users.uindex()
        Users.usecindex()
        print("User modified")

class Ratings():

    def __init__(self, username, movieId, rating, reviews):
        self.username = username
        self.movieId = movieId
        self.rating = rating
        self.reviews = reviews

    @staticmethod
    def get_all_ratings(movieId):
        movieId = int(movieId)
        df_ratings = pd.read_csv(path + "/data/ratings.csv")
        df_ratings = df_ratings.loc[df_ratings['movieId'] == movieId]
        if movieId in list(df_ratings['movieId']):
            df_ratings = df_ratings.drop(['movieId'], axis=1)
            df_user = pd.read_csv(path + "/data/user.csv")
            id2 = df_ratings['userId']
            a = df_user.set_index('userId')['name'].to_dict()
            b = df_ratings.filter(like='userId')
            df_ratings[b.columns] = b.replace(a)
            df_ratings = df_ratings.rename(columns={'userId': 'username'})
            print(df_ratings)
            rating_obj = list()
        for index, row in df_ratings.iterrows():
            rating_obj.append(Ratings(row['username'],'', row['ratings'],row['reviews']))
        return rating_obj

    #Check if user has left a rating for movie
    @staticmethod
    def check_rating(user_id, movieId):
        Ratings.rindex()
        Ratings.rsecindex()
        dpk_ratings = pd.read_csv(path + "/data/rprimary.csv", usecols=[0, 1], header=None)
        a = list(dpk_ratings.to_records(index=False))
        a1 = 0
        id1, movieid = str(user_id), str(movieId)
        x = (id1, movieid)
        for (index, tuple) in enumerate(a[1:]):
            if tuple[0] == id1 and tuple[1] == movieid:
                a1 = 1
                break
        if (a1):
            return True
        else:
            return False

    @staticmethod
    def rindex():
        Offset_address = []
        Primary_key = []
        movieId = []
        csv_columns = ["userId", "movieId", "offset"]
        fi_ratings = open(path + "/data/ratings.csv", "r", encoding='utf-8')
        pos = fi_ratings.tell()
        line = fi_ratings.readline()
        pos = fi_ratings.tell()
        line = fi_ratings.readline()
        while line:
            a = line.split(",")
            # print(a)
            # print(pos,",",a[0],",",a[1])
            Offset_address.append(pos)
            Primary_key.append(a[0])
            movieId.append(a[1])
            pos = fi_ratings.tell()
            line = fi_ratings.readline()
        list = [Primary_key, movieId, Offset_address]
        list = zip_longest(*list, fillvalue='')
        export_data = sorted(list, key=lambda x: x[0])
        with open(path + '/data/rprimary.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(("userId", "movieId", "offset"))
            wr.writerows(export_data)
        myfile.close()

    @staticmethod
    def rsecindex():
        ratings = []
        Primary_key = []
        csv_columns = ["ratings", "id"]
        fi_ratings = open(path + "/data/ratings.csv", "r", encoding='utf-8')
        pos = fi_ratings.tell()
        line = fi_ratings.readline()
        pos = fi_ratings.tell()
        line = fi_ratings.readline()
        while line:
            line = line.rstrip()
            temp = line.split(",")
            ratings.append(temp[2])
            Primary_key.append(temp[0] + '|' + temp[1])
            pos = fi_ratings.tell()
            line = fi_ratings.readline()
        list = [ratings, Primary_key]
        list = zip_longest(*list, fillvalue='')
        export_data = sorted(list, key=lambda x: x[0])
        with open(path + "/data/rsecondary.csv", 'w', encoding="ISO-8859-1", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(("ratings", "id"))
            wr.writerows(export_data)
        myfile.close()

    @staticmethod
    def rinsert(id1, movieid, ratings, reviews):
        movieid = int(movieid)
        id1 = int(id1)
        Ratings.rindex()
        Ratings.rsecindex()
        with open(path + '/data/ratings.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow('')
            filedname = [id1, movieid, ratings, reviews]
            writer = csv.writer(csvfile, lineterminator='')
            writer.writerow(filedname)
        csvfile.close()
        df_movies = pd.read_csv(path + "/data/movies.csv")
        df_movies = df_movies.loc[df_movies['movieId'] == movieid]
        no_of_ratings = int(df_movies['no_of_ratings']) + 1
        df_movies = pd.read_csv(path + "/data/\movies.csv")

        df_ratings = pd.read_csv(path + "/data/ratings.csv")
        df_ratings = df_ratings.loc[df_ratings['movieId'] == movieid]
        t = 0
        if movieid in list(df_ratings['movieId']):
            for i in list(df_ratings['ratings']):
                t += i
        if t:
            t /= len(df_ratings.index)
            t = str(round(t, 2))
        iu = df_movies.query('movieId == @movieid').index
        df_movies.loc[iu, ['average_ratings', 'no_of_ratings']] = [t, no_of_ratings]
        df_movies.to_csv(path + "/data/movies.csv", index=False)
        print('done')
        Ratings.rindex()
        Ratings.rsecindex()

    @staticmethod
    def rdelete(uid, movieid):
        movieid = int(movieid)
        uid = int(uid)
        df_ratings = pd.read_csv(path + "/data/ratings.csv")
        i = df_ratings.query('userId == @uid & movieId == @movieid').index
        df_ratings = df_ratings.drop(i)
        print(df_ratings)
        df_ratings.to_csv(path + "/data/ratings.csv", index=False)
        file_data = open(path + "/data/ratings.csv", 'rb').read()
        open(path + "/data/ratings.csv", 'wb').write(file_data[:-2])

        df_movies = pd.read_csv(path + "/data/movies.csv")
        df_movies = df_movies.loc[df_movies['movieId'] == movieid]
        no_of_ratings = int(df_movies['no_of_ratings'].values[0]) - 1
        df_movies = pd.read_csv(path + "/data/\movies.csv")

        df_ratings = pd.read_csv(path + "/data/ratings.csv")
        df_ratings = df_ratings.loc[df_ratings['movieId'] == movieid]
        t = 0
        if movieid in list(df_ratings['movieId']):
            for i in list(df_ratings['ratings']):
                t += i
        if t:
            t /= len(df_ratings.index)
            t = str(round(t, 2))
        iu = df_movies.query('movieId == @movieid').index
        df_movies.loc[iu, ['average_ratings', 'no_of_ratings']] = [t, no_of_ratings]
        df_movies.to_csv(path + "/data/movies.csv", index=False)
        Ratings.rindex()
        Ratings.rsecindex()

    @staticmethod
    def rupdate(uid, movieid, ratings, reviews):
        movieid = int(movieid)
        uid = int(uid)
        df_ratings = pd.read_csv(path + "/data/ratings.csv")
        iu = df_ratings.query('userId == @uid & movieId == @movieid').index
        df_ratings.loc[iu, ['ratings', 'reviews']] = [ratings, reviews]
        df_ratings.to_csv(path + "/data/ratings.csv", index=False)
        df_movies = pd.read_csv(path + "/data/movies.csv")
        # -------------
        df_ratings = pd.read_csv(path + "/data/ratings.csv")
        df_ratings = df_ratings.loc[df_ratings['movieId'] == movieid]
        t = 0
        if int(movieid) in list(df_ratings['movieId']):
            for i in list(df_ratings['ratings']):
                t += i
        if t:
            t /= len(df_ratings.index)
            t = str(round(t, 2))
        iu = df_movies.query('movieId == @movieid').index
        df_movies.loc[iu, ['average_ratings']] = [t]
        df_movies.to_csv(path + "/data/movies.csv", index=False)
        # --------------
        Ratings.rindex()
        Ratings.rsecindex()
        print("Modification Successful ")

class Admin(UserMixin):

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    '''@staticmethod
    def check_admin(adminId):
        adminId = int(adminId)
        if adminId != 1234:
            return False
        return True'''

    @staticmethod
    def check_password(adminId, password):
        adminId = adminId
        if str(password) == '1234' and str(adminId) == '1234':
            return True
        else:
            return False

    @staticmethod
    def get(adminId):
        #if adminId == '1234' and password == '1234':
        return Admin(adminId, 'admin', '1234')
        #else:
            #return None
