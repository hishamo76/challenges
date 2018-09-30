import csv
from collections import defaultdict, namedtuple
from operator import attrgetter
import os
from urllib.request import urlretrieve
import numpy as np

# BASE_URL = 'http://projects.bobbelderbos.com/pcc/movies/'
# TMP = '.'

fname = r'movie_metadata.csv'
# remote = os.path.join(BASE_URL, fname)
# local = os.path.join(TMP, fname)
# urlretrieve(remote, local)

# MOVIE_DATA = local
MIN_MOVIES = 4
MIN_YEAR = 1960

Movie = namedtuple('Movie', 'title year score')


def main():
    directors = get_movies_by_director()
    avg_list = get_average_scores(directors)
    avg_list.sort(reverse=True, key=myFun)
    print_top_twenty(directors, avg_list[:20])
    

def print_top_twenty(directors, movies):
    for index, value in enumerate(movies):
        print("{0:02}. {1[0]:<53}{1[1]}".format(index+1, value))
        print("-"*60)
        print_movies_by_director(directors[value[0]])
        print()

def print_movies_by_director(director_movies):
    mov_sorted = sorted(director_movies, key=attrgetter('score'), reverse=True)
    for mov in mov_sorted:
        print("{}] {:<50} {}".format(mov.year, mov.title, mov.score))




def get_movies_by_director(data=fname):
    """Extracts all movies from csv and stores them in a dict,
    where keys are directors, and values are a list of movies,
    use the defined Movie namedtuple"""
    directors = defaultdict(list)
    with open(data, encoding='utf-8') as csv_file:
        for line in csv.DictReader(csv_file):
            try:
                director = line['director_name']
                movie = line['movie_title'].replace('\xa0', '') #\xa0 is unicode for space
                year = int(line['title_year'])
                score = float(line['imdb_score'])
            except ValueError:
                continue # if data has bad values, skip it

            m = Movie(title=movie, year=year, score=score)
            directors[director].append(m)
    return directors


def _calc_mean(movies):
    """Helper method to calculate mean of list of Movie namedtuples,
       round the mean to 1 decimal place"""
    avg = []
    for movie in movies:
        avg.append(float(movie.score))
    return round(np.mean(avg), 1)



def get_average_scores(directors):
    """Iterate through the directors dict (returned by get_movies_by_director),
       return a list of tuples (director, average_score) ordered by highest
       score in descending order. Only take directors into account
       with >= MIN_MOVIES"""
    average_list = []
    for director, movies in directors.items():
        if len(movies) >= MIN_MOVIES:
            avg_movie = _calc_mean(movies)
            average_list.append((director, avg_movie))
        else:
            continue
    
    return sorted(average_list, key= lambda tup: tup[1], reverse=True)
        
def myFun(e):
    return e[1]



if __name__ == "__main__":
    main()
