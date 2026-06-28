import os
from collections import Counter

import pandas as pd
from matplotlib import pyplot as plt

W = '\033[0m'
R = '\033[31m'
G = '\033[32m'
O = '\033[33m'
B = '\033[34m'
P = '\033[35m'

FILM_CSV_CANDIDATES = ['ld_collection.csv', 'LD_collection.csv', 'collection.csv']
GAME_CSV_CANDIDATES = ['games_2026.csv', 'games.csv', 'collection.csv']

FILM_CSV_PATH = None
GAME_CSV_PATHS = []


def detect_csv_type(path):
    try:
        df = pd.read_csv(path, encoding='utf8', nrows=0)
    except Exception:
        return None

    headers = [c.strip() for c in df.columns]
    if 'Game' in headers and 'System' in headers:
        return 'game'
    if {'Title', 'Genre', 'Release'}.issubset(set(headers)):
        return 'film'
    return None


def initialize_paths():
    global FILM_CSV_PATH, GAME_CSV_PATHS, GAMES_LIST_PATH
    for candidate in FILM_CSV_CANDIDATES:
        if os.path.isfile(candidate) and detect_csv_type(candidate) == 'film':
            FILM_CSV_PATH = candidate
            break

    if FILM_CSV_PATH is None:
        print(R + 'Warning: No film CSV file detected. Looking for:', FILM_CSV_CANDIDATES)

    for candidate in GAME_CSV_CANDIDATES:
        if os.path.isfile(candidate) and detect_csv_type(candidate) == 'game':
            GAME_CSV_PATHS.append(candidate)

    if not GAME_CSV_PATHS:
        print(R + 'Warning: No game CSV file detected from:', GAME_CSV_CANDIDATES)


initialize_paths()


def menu():
    print("")
    print(W + "*********************************************************")
    print("")
    print(P + "             ENTER: 0 - 10 to choose an action           ")
    print("")
    print(W + "*********************************************************")
    print("")
    # Film-related actions
    print(B + f' - 1 View full film collection ({FILM_CSV_PATH or "none"})')
    print(G + ' - 2 Search film by title')
    print(P + ' - 3 Search films by genre')
    print(W + ' - 4 Search films by release year')
    print(B + ' - 5 Graph film genre popularity')
    # Game-related actions
    print(G + f' - 6 View full video game collection ({", ".join(GAME_CSV_PATHS) or "none"})')
    print(O + ' - 7 Search video game by title')
    print(G + ' - 8 Total number of video games')
    print(P + ' - 9 Graph video games by system')
    print(B + ' - 10 Load a new games CSV file')
    print("<--------->")
    print(R + ' - 0 Quit')
    print(W + '_________________________________________________________')
    print("")


def load_films():
    if FILM_CSV_PATH is None:
        print(R + 'No film CSV path has been detected.')
        return None

    try:
        return pd.read_csv(FILM_CSV_PATH, encoding='utf8')
    except FileNotFoundError:
        print(R + f'Error: {FILM_CSV_PATH} not found.')
        return None
    except Exception as exc:
        print(R + f'Error reading film CSV {FILM_CSV_PATH}: {exc}')
        return None


def load_game_file(path):
    try:
        df = pd.read_csv(path, encoding='utf8')
    except FileNotFoundError:
        return None
    except Exception:
        return None

    if 'Game' in df.columns and 'System' in df.columns:
        return df[['Game', 'System']].copy()

    if len(df.columns) >= 2:
        df = df.iloc[:, :2].copy()
        df.columns = ['Game', 'System']
        return df

    return None


def load_games():
    if not GAME_CSV_PATHS:
        print(R + 'No game CSV sources are configured.')
        return None

    frames = []
    for path in GAME_CSV_PATHS:
        frame = load_game_file(path)
        if frame is None:
            print(R + f'Warning: {path} could not be read as a game CSV.')
            continue
        frames.append(frame)

    if not frames:
        return None

    result = pd.concat(frames, ignore_index=True)
    result.drop_duplicates(inplace=True)
    return result


def set_games_csv():
    global GAME_CSV_PATHS
    path = input('Enter new games CSV filename or path: ').strip()
    if not path:
        print(R + 'No file path entered.')
        return

    if not os.path.isfile(path):
        print(R + f'Error: {path} not found.')
        return

    if detect_csv_type(path) != 'game':
        print(R + f'Error: {path} does not appear to be a games CSV.')
        return

    GAME_CSV_PATHS = [path]
    print(G + f'Loaded new games CSV: {path}')


def view_films():
    df = load_films()
    if df is None:
        return
    print(df.to_string(index=False))


def search_films_by_title():
    df = load_films()
    if df is None:
        return

    query = input('Enter film title: ').strip()
    result = df[df['Title'] == query]
    print(result.to_string(index=False) if not result.empty else R + 'No film found with that title.')


def total_video_games():
    df = load_games()
    if df is None:
        return
    print(G + f'There are {len(df)} video games in the database.')


def search_films_by_genre():
    df = load_films()
    if df is None:
        return

    print()
    print('Search is case sensitive. Examples: Action, Anime, Comedy, Drama, Family, Holiday, Romance')
    genre = input('Enter genre: ').strip()
    result = df[df['Genre'] == genre]
    print(result.to_string(index=False) if not result.empty else R + 'No films found for that genre.')


def search_films_by_year():
    df = load_films()
    if df is None:
        return

    year = input('Enter release year: ').strip()
    result = df[df['Release'] == year]
    print(result.to_string(index=False) if not result.empty else R + 'No films found for that release year.')


def plot_film_genres():
    df = load_films()
    if df is None:
        return

    genre_counter = Counter()
    for genre in df['Genre'].dropna():
        genre_counter.update([g.strip() for g in genre.split(',') if g.strip()])

    if not genre_counter:
        print(R + 'No genre data available to plot.')
        return

    genres, counts = zip(*genre_counter.most_common(10))
    plt.style.use('bmh')
    plt.barh(list(reversed(genres)), list(reversed(counts)))
    plt.title('Top 10 Most Popular Film Genres')
    plt.xlabel('Number of Films')
    plt.tight_layout()
    plt.show()


def plot_game_systems():
    df = load_games()
    if df is None:
        return

    system_counter = Counter()
    for system in df['System'].dropna():
        system_counter.update([s.strip() for s in system.split(',') if s.strip()])

    if not system_counter:
        print(R + 'No system data available to plot.')
        return

    systems, counts = zip(*system_counter.most_common(15))
    plt.style.use('bmh')
    plt.barh(list(reversed(systems)), list(reversed(counts)))
    plt.title('Video Game Systems with the Most Games')
    plt.xlabel('Number of Games')
    plt.tight_layout()
    plt.show()


def view_games():
    df = load_games()
    if df is None:
        return
    print(df.to_string(index=False))


def search_games_by_title():
    df = load_games()
    if df is None:
        return

    query = input('Enter game title: ').strip()
    result = df[df['Game'] == query]
    print(result.to_string(index=False) if not result.empty else R + 'No game found with that title.')


def main():
    while True:
        menu()
        try:
            option = int(input('Enter your choice: ').strip())
        except ValueError:
            print(R + 'Invalid input. Enter a number between 0 and 10.')
            continue

        if option == 0:
            print(G + 'Thanks for checking it out, PEACE!')
            break
        # Film actions
        elif option == 1:
            view_films()
        elif option == 2:
            search_films_by_title()
        elif option == 3:
            search_films_by_genre()
        elif option == 4:
            search_films_by_year()
        elif option == 5:
            plot_film_genres()
        # Game actions
        elif option == 6:
            view_games()
        elif option == 7:
            search_games_by_title()
        elif option == 8:
            total_video_games()
        elif option == 9:
            plot_game_systems()
        elif option == 10:
            set_games_csv()
        else:
            print(R + 'Not an option hoss!')


if __name__ == '__main__':
    main()
