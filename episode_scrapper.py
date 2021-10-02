import requests
import re
import sys
import os
import pickle
import itertools
import time
import threading
from bs4 import BeautifulSoup


class EpisodeData:
    """
    An object for reading the episode data from IMDB

    Attributes:
    ---------------
    season_length:   The number of seasons released
    episode_data:    Full episode data. 2D dictionary.
                     First keys are the season numbers.
                     Second keys are the episode numbers
    """
    def __init__(self):
        self.season_length = 0
        self.episode_data = dict()
        if not os.path.exists('episode_data.pickle'):
            self.update()
        else:
            self.get_episode_data()

    def update(self):
        """Creates a new pickle file from scratch, scraps the
        episode info from IMDB and dumbs it into the pickle file"""
        pickle_file = open('episode_data.pickle', 'wb')
        self.scrapping_process()
        pickle.dump(self.episode_data, pickle_file)
        pickle_file.close()

    def scrap(self):
        """Scraps IMDB for episode data"""
        main_string = 'https://www.imdb.com/title/tt2861424/episodes?season={}'
        season_index = 1
        while True:
            single_season_data = dict()
            web_string = main_string.format(season_index)
            page = requests.get(web_string)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find_all('div', class_='info')
            for index, episode in enumerate(results, start=1):
                episode_name = episode.find('a').text
                if re.match(r"Episode #[0-9]", episode_name):
                    break
                else:
                    single_season_data[index] = episode_name
            if len(single_season_data):
                self.episode_data[season_index] = single_season_data
            else:
                break
            season_index += 1

    def scrapping_process(self):
        """The only method that calls scrap method. Created for string animations"""
        done = False

        def animate():
            for c in itertools.cycle(['|', '/', '-', '\\']):
                if done:
                    break
                sys.stdout.write('\rLoading Episodes ' + c)
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write('\rDone!                                                ')
            sys.stdout.write(f'\nLast existing season: Season {self.season_length}')

        t = threading.Thread(target=animate)
        t.start()
        time.sleep(1)
        self.scrap()
        self.season_length = len(self.episode_data)
        done = True

    def get_episode_data(self):
        """Reads the episode data information the pickle file"""
        pickle_file = open('episode_data.pickle', 'rb')
        self.episode_data = pickle.load(pickle_file)
        pickle_file.close()

