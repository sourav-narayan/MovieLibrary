from update import *
import pandas as pd

uid = -1
path = str(pathlib.Path().absolute())

def recommendationtop():
    df2 = pd.read_csv(path+'/data/movies.csv')
    #print(df2)
    df2 = df2.drop(['description'],axis=1)
    C=df2['average_ratings'].mean()
    m = df2['no_of_ratings'].quantile(0.9)
    q_movies = df2.copy().loc[df2['no_of_ratings'] >= m]
    q_movies.shape
    #print(q_movies.shape)

    def weighted_rating(x, m=m, C=C):
        v = x['no_of_ratings']
        R = x['average_ratings']
        # Calculation based on the IMDB formula
        return (v/(v+m) * R) + (m/(m+v) * C)

    q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
    q_movies = q_movies.sort_values('score', ascending=False)

    #Print the top 15 movies
    return(q_movies.head(5))
