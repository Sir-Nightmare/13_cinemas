import argparse
import requests

from bs4 import BeautifulSoup
from requests.exceptions import Timeout, ConnectionError

MIN_NUM_OF_CINEMAS = 10


def fetch_afisha_page():
    url = 'http://www.afisha.ru/msk/schedule_cinema/'
    return requests.get(url).content


def parse_afisha_list(raw_html, min_cinemas=10):
    soup = BeautifulSoup(raw_html, 'lxml')
    raw_divs = soup.find('div', id='schedule').find_all('div', class_='object')
    movies_list = []
    for div in raw_divs:
        movie_title = div.find('h3', {'class': 'usetags'}).a.text
        cinemas_num = len(div.find('table').find_all('tr'))
        if cinemas_num > min_cinemas:
            movies_list.append({'title': movie_title, 'cinemas': cinemas_num})
    return movies_list


def get_movie_page(movie, url, headers, session):
    params = {'first': 'yes', 'kp_query': movie}
    try:
        return session.get(url, params=params, headers=headers, timeout=10).content
    except (Timeout, ConnectionError):
        exit('Maybe we\'re banned, try later')


def get_rate_votes(page):
    soup = BeautifulSoup(page, 'lxml')
    rate = soup.find('span', class_='rating_ball')
    rate = float(rate.text) if rate else 0
    votes = soup.find('span', class_='ratingCount')
    votes_num = int(votes.text.replace('\xa0', '')) if votes else 0
    return {'rate': rate, 'votes': votes_num}


def collect_info(movies_list):
    movies_info = []
    url = 'http://kinopoisk.ru/index.php'
    headers = {
        'Host': 'www.kinopoisk.ru:443',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': 'https://www.kinopoisk.ru/s/',
        'upgrade-insecure-requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, \
        like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    session = requests.session()
    for movie in movies_list:
        movie_page = get_movie_page(movie['title'], url, headers, session)
        movie_rate = get_rate_votes(movie_page)
        movies_info.append({'title': movie['title'],
                            'cinemas': movie['cinemas'],
                            'rate': movie_rate['rate'],
                            'votes': movie_rate['votes']
                            })
    return movies_info


def output_movies_list(movies_list):
    print('Movies with the highest rating:\r\n')
    print('{4:2}{5:>2s}{4:^3}{0:^43s}{4:^3}{1:6s}{4:^3}{2:>6s}{4:^3}{3:7s}{4:>2}'.format(
        'Movie', 'rating', 'votes', 'cinemas', '|', '#'))
    print(80 * '-')
    for line, movie in enumerate(reversed(best_movies), 1):
        print('{4:2}{5:>2d}{4:^3}{0:43s}{4:^3}{1:<6g}{4:^3}{2:>6d}{4:^3}{3:>7d}{4:>2}'.format(
            movie['title'], movie['rate'], movie['votes'], movie['cinemas'], '|', line))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cinemas', default=10, type=int,
                        help='min number of cinemas with the movie, default = 10')
    parser.add_argument('-c', '--movies', default=10, type=int,
                        help='number of movies to show, default = 10')
    args = parser.parse_args()
    raw_html = fetch_afisha_page()
    movies_list = parse_afisha_list(raw_html, args.cinemas)
    number_of_movies = len(movies_list)
    print('{} films were found. Downloading rating info started.\r\n'.format(number_of_movies))
    amount_to_show = args.movies if args.movies < number_of_movies else number_of_movies
    moves_info = collect_info(movies_list)
    best_movies = sorted(movies_list, key=lambda x: x['rate'])[-amount_to_show:]
    output_movies_list(best_movies)
