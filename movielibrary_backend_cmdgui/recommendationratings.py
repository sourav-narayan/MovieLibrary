from update import *
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


uid = -1
path = str(pathlib.Path().absolute())


def recommendationname(movie_name):
    movies = pd.read_csv(path + '\\data\\movies.csv')
    ratings = pd.read_csv(path + '\\data\\ratings.csv')
    #print(movies)
    #print(ratings)
    final_dataset = ratings.pivot(index='movieId', columns='userId', values='ratings')
    final_dataset.fillna(0, inplace=True)
    #print(final_dataset)

    csr_data = csr_matrix(final_dataset.values)
    #print(csr_data)

    final_dataset.reset_index(inplace=True)
    knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
    knn.fit(csr_data)

    n_movies_to_reccomend = 10
    movie_list = movies[movies['title'].str.contains(movie_name)]
    if len(movie_list):
        movie_idx= movie_list.iloc[0]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
        distances , indices = knn.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_reccomend+1)
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]['movieId']
            idx = movies[movies['movieId'] == movie_idx].index
            recommend_frame.append({'movieId':movies.iloc[idx]['movieId'].values[0],'img':movies.iloc[idx]['img'].values[0],'title':movies.iloc[idx]['title'].values[0],'genre':movies.iloc[idx]['genre'].values[0],'distance':val[1]})
        df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_reccomend+1))
        return df.head(5)
    else:
        return "No movies found. Please check your input"



