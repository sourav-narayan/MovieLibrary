import re
from update import *
import pandas as pd

uid = -1
path = str(pathlib.Path().absolute())


def recommendationgenre(genre, percentile=0.85):
    #df = gen_md[gen_md['genre'] == genre]
    features = 'genre'
    md = pd.read_csv(path + '/data/movies.csv')
    s = md.apply(lambda x: pd.Series(x['genre']), axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'genre'
    gen_md = md.drop('genre', axis=1).join(s)
    #print(gen_md)

    df = gen_md[gen_md['genre'].str.contains(genre, flags=re.IGNORECASE)]
    #print(df)
    C = df['average_ratings'].mean()
    m = df['no_of_ratings'].quantile(percentile)
    #print(vote_counts.values,vote_averages.values)

    qualified = df[(df['no_of_ratings'] >= m) & (df['no_of_ratings'].notnull()) & (df['average_ratings'].notnull())][['movieId','img','title', 'genre','no_of_ratings', 'average_ratings']]
    qualified['no_of_ratings'] = qualified['no_of_ratings'].astype('int')
    qualified['average_ratings'] = qualified['average_ratings'].astype('int')

    qualified['wr'] = qualified.apply(lambda x: (x['no_of_ratings'] / (x['no_of_ratings'] + m) * x['average_ratings']) + (m / (m + x['no_of_ratings']) * C),axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(250)

    return qualified
print(recommendationgenre('drama',0))