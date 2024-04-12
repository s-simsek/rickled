import webbrowser
import sys
import time


def get_key(string, dictionary: dict) -> list:
    """
    Gets the key from 2D dictionary for the given string
    @param string: string value to look for
    @param dictionary: a 2D dictionary
    @return: a 2 element list
    >>> from episode_scrapper import EpisodeData
    >>> get_key("Pickle Rick", EpisodeData().main_data)
    [3, 3]
    """
    for season_number, season_dict in dictionary.items():
        for episode_number, episode_name in season_dict.items():
            if string == episode_name:
                return [season_number, episode_number]


def key_getter(val, my_dict: dict):
    """Gets the key of the value from a dictionary
    >>> test = {1: 'rick', 2: 'morty', 3: 'beth', 4: 'jerry'}
    >>> key_getter('rick', test)
    1
    >>> key_getter('morty', test)
    2
    """
    for key, value in my_dict.items():
        if val == value:
            return key


def dizibox():
    """Directs the user to www.dizibox.pw"""
    def nested(season, episode):
        with_season = 'https://www.dizibox.pw/rick-and-morty-' + str(season) + '-sezon-'
        with_episode = with_season + str(episode) + '-bolum-izle/'
        webbrowser.open(with_episode)

    return nested


def dizilab():
    """Directs the user to www.dizilab.pw"""
    def nested(season, episode):
        season = str(season)
        leading_to_episode = 'https://dizilab.pw/rick-and-morty/sezon-' + season + '/bolum-'
        episode = str(episode)
        desired_episode = leading_to_episode + episode
        webbrowser.open(desired_episode)
    return nested


def yabancidizi():
    """Directs the user to www.yabancidizi.org"""
    def nested(season, episode):
        season = str(season)
        string = "https://yabancidizi.vip/dizi/rick-and-morty-izle-2/sezon-" + season
        string += "/bolum-" + str(episode)
        webbrowser.open(string)
    return nested

# TODO: Add extra episode providers


def animation():
    anim = "|/-\\"
    for i in range(40):
        time.sleep(0.1)
        sys.stdout.write("\r" + anim[i % len(anim)])
        sys.stdout.flush()
    print("End!")


def text(string, loop_quantity=4, dot_number=3):
    loading_speed = 0.45
    loading_string = "." * dot_number
    print(string, end="")
    while loop_quantity:
        for index, char in enumerate(loading_string):
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(loading_speed)
        index += 1
        sys.stdout.write("\b" * index + " " * index + "\b" * index)
        sys.stdout.flush()
        loop_quantity -= 1


if __name__ == "__main__":
    import doctest
    doctest.testmod()
