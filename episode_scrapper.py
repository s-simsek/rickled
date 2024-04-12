import requests
import re
import sys
import os
import pickle
import itertools
import time
import threading
from bs4 import BeautifulSoup

MAIN_URL = "https://www.imdb.com/title/tt2861424/episodes/?ref_=tt_ov_epl"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
SEASON_URL = "https://www.imdb.com/title/tt2861424/episodes/?season="
SEASON_CLASS = "ipc-tabs ipc-tabs--base ipc-tabs--align-left ipc-tabs--display-chip ipc-tabs--inherit"
EPISODE_INFO_CLASS = "sc-aafba987-1 khlUsN"
IMG_CLASS = "ipc-slate ipc-slate--base ipc-slate--dynamic-width sc-aafba987-2 cCFDaN ipc-sub-grid-item ipc-sub-grid-item--span-4"
IMG_INDEX = -1
RATING_CLASS = "sc-e2dbc1a3-0 ajrIH sc-282bae8e-3 bXuGWE"
CONTENT_CLASS = "ipc-html-content-inner-div"
TITLE_CLASS = "ipc-title__text"


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
        self.main_data = dict()
        if not os.path.exists('episode_data.pickle'):
            self.update()
        else:
            self.get_episode_data()

    def update(self):
        """Creates a new pickle file from scratch, scraps the
        episode info from IMDB and dumbs it into the pickle file"""
        pickle_file = open('episode_data.pickle', 'wb')
        self.scrapping_process()
        pickle.dump(self.main_data, pickle_file)
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
                self.main_data[season_index] = single_season_data
            else:
                break
            season_index += 1

    @staticmethod
    def extract_urls(text):
        pattern = r'https://.*?\.jpg'
        urls = re.findall(pattern, text)
        return urls

    @staticmethod
    def extract_season_numbers(long_string):
        pattern = r'season=(\d+)'
        season_numbers = re.findall(pattern, long_string)
        return season_numbers

    def scrap_v2(self):
        response = requests.get(MAIN_URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        season_info = soup.find_all('div', class_=SEASON_CLASS)
        season_numbers = self.extract_season_numbers(season_info[0].prettify())

        #main_data = {}
        stop = False
        for season_num in season_numbers:
            season_response = requests.get(SEASON_URL + season_num, headers=HEADERS)
            season_html = BeautifulSoup(season_response.text, 'html.parser')
            episodes = season_html.find_all('div', class_=EPISODE_INFO_CLASS)

            episode_data = {}
            for episode_idx, episode in enumerate(episodes, start=1):
                episode_info = {}
                try:
                    episode_info['title'] = episode.find(class_=TITLE_CLASS).get_text().split('∙ ')[-1]
                    episode_info['content'] = episode.find(class_=CONTENT_CLASS).get_text()
                    episode_info['rating'] = episode.find(class_=RATING_CLASS).find('span')['aria-label'].split(":")[
                        1].strip()
                    episode_info['image_url'] = self.extract_urls(episode.find(class_=IMG_CLASS).prettify())[IMG_INDEX]
                except:
                    stop = True
                if stop:
                    break
                else:
                    episode_data[episode_idx] = episode_info
            if episode_data:
                self.main_data[season_num] = episode_data
            if stop:
                break

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
        self.scrap_v2()
        self.season_length = len(self.main_data)
        done = True

    def get_episode_data(self):
        """Reads the episode data information the pickle file"""
        pickle_file = open('episode_data.pickle', 'rb')
        self.main_data = pickle.load(pickle_file)
        pickle_file.close()
