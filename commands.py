"""All the classes necessary for the 'watch', 'precise', and 'switch' command"""
import random
import re
import os
import subprocess as sp
from utils import *
from copy import deepcopy
from typing import Set


class History:
    """
    -- duals: Episodes to be watched
    -- full_season_info: All the present episodes
    -- watched: watched episodes, written in the history.txt
    """

    def __init__(self, full_data: dict):
        self.duals = dict()
        self.full_season_info = full_data
        if not os.path.exists('history.txt'):
            file = open("history.txt", mode="w")
            file.close()
        self.watched = dict()
        self.get_data()  # A method to record watched episodes

    @staticmethod
    def record(season, episode):
        """Record the episode data to history.txt"""
        with open('history.txt', mode='a') as f:
            f.write('season {} episode {}\n'.format(season, episode))

    @staticmethod
    def delete_record(amount):
        """Delete the given 'amount' of episodes from history.txt
        @param amount: either integer or 'all'
        """
        with open("history.txt", mode='r') as f:
            watched_episodes = f.readlines()
            if amount == 'all':
                watched_episodes = []
            else:
                del watched_episodes[-amount:]
        with open("history.txt", mode='w') as f:
            for i in watched_episodes:
                f.write(i)

    def look_back(self, last):
        """
        Shows the history of watched episodes
        @param last: can only be an integer or 'all', indicating the amount of
                    watched episodes to display
        """
        with open("history.txt", mode='r') as watched:
            watched_episodes = watched.readlines()
            watched_episodes.reverse()
        if last == 'all' and len(watched_episodes) == 0:
            print('\nYou do not have a history yet!')
        elif last != 'all' and last > len(watched_episodes):
            print('\nYou do not have that much history!')
        else:
            if last == 'all':
                print('\n\t---All the episodes you have watched---\n')
            else:
                print('\nThe last {} episodes you watched:'.format(last))
            for i in range(len(watched_episodes) if last == 'all' else last):
                info = re.split("season|episode|\n", watched_episodes[i])
                info = tuple([int(x) for x in info if x])
                season_number, episode_number = info
                episode = self.full_season_info[season_number][episode_number]
                print("From Season {}, Episode {}: '{}'".format(season_number, episode_number, episode))

    def get_data(self):
        """Reads and saves the episodes history from history.txt into self.watched"""
        with open('history.txt', mode='r') as f:
            all_watched = f.readlines()
        for i in range(len(all_watched)):
            info = re.split('season|episode|\n', all_watched[i])
            info = tuple([int(x) for x in info if x])
            season_number, episode_number = info
            self.watched[len(self.watched.keys()) + 1] = [season_number, episode_number]


class Watch(History):
    """
    -- episode_quantity: Number of episodes to be watched, selected by the user
    -- provider: The numeric for the website provider
    -- providers: Available providers
    -- removal: Season numbers to removed, selected by the user if desired
    """

    def __init__(self, data):
        super().__init__(data)
        self.episode_quantity = 0
        self.provider = 0
        self.providers = [0, 1, 2]  # TODO: add extra providers here
        self.removal = {}

    def input_corrector(self, user_input, selected_season=None,
                        binary=False, season=False, episode=False,
                        removing=False, provider=False) -> int:
        """
        An input correction method
        @param user_input: user input, a string value
        @param selected_season: selected season by the user, an integer, already validated
        @param binary: if True, forces the user to provide a binary number
        @param season: If True, forces the user to provide a valid season number
        @param episode: If True, forces the user to provide a valid episode number
                        If True, selected_season has to be provided
        @param removing: True when user wants to remove a season from existing seasons
        @param provider: If True, forces the user select an existing provider
        @return: the corrected input, an int value
        """
        # TODO: try to create a separate input corrector for each usage form, i.e., season,
        #       episode, removing, provider
        #       You can also create a different custom exception for argument errors like
        #       ProviderCommandError, EpisodeCommandError, SeasonCommandError, RemovalCommandError
        while type(user_input) == str:
            if user_input == 'exit':
                sys.exit()
            if user_input == 'clear':
                sp.call('cls', shell=True)
            try:
                user_input = int(user_input)
                if user_input <= 0 and not binary and not provider:
                    raise ValueError
                elif binary and user_input not in [0, 1]:
                    raise ValueError
                elif season:
                    if user_input in self.full_season_info and not removing:
                        print('Good Choice, Sir \n')
                    else:
                        raise ValueError
                elif provider:
                    if user_input not in self.providers:
                        print('Please, enter a valid provider number')
                        user_input = input('> ')
                elif episode:
                    if user_input not in list(self.full_season_info[selected_season].keys()):
                        print('\nPlease, enter a valid episode number')
                        user_input = input('> ')
            except ValueError:
                print("\nPlease, enter a valid number")
                user_input = input("> ")
        return user_input

    def direct_website(self, quantity):
        """Directs the user to Rick and Morty provider"""
        for episode_info in self.duals.values():
            print('And awaaay we go!')
            season, episode = episode_info
            self.record(season, episode)
            self.set_provider()(season, episode)
            quantity -= 1
            if quantity != 0:
                print("\nWould you like to continue watching the next recommended episode?")
                print("Yes:1 No:0")
                watching = self.input_corrector(input("> "), binary=True)
                if watching:
                    continue
                else:
                    print('Okay, see you soon!')
                    break

    def set_provider(self):
        """Sets the Rick and Morty episode provider"""
        if self.provider == 0:
            return yabancidizi()
        elif self.provider == 1:
            return dizibox()
        elif self.provider == 2:
            return dizilab()
        # TODO: add providers here and below as well
        #  rather than elif cases, think about another data structure to do in less line of codes

    def switch(self):
        """Switches the Rick and Morty provider
        0 -> yabancidizi.vip
        1 -> dizibox.pw
        2 -> dizilab.pw
        """
        print('\nWhich provider would you like to chose?')
        print('Currently your provider is provider ' + str(self.provider))
        print('0 -> yabancidizi.vip')
        print('1 -> dizibox.pw')
        print('2 -> dizilab.pw')
        self.provider = self.input_corrector(input('> '), provider=True)

    def removal_input_corrector(self, user_input) -> Set[int]:
        """
        Forces the user to provide a valid season number(s) for removal
        @return: List, containing season number(s) for removal
        """
        while True:
            if user_input == 'exit':
                sys.exit()
            if user_input == 'clear':
                sp.call('cls', shell=True)
            user_input = re.split(',|and', user_input)
            try:
                user_input = set(int(x) for x in user_input)
                invalid_seasons = [i for i in user_input if i not in self.full_season_info.keys()]
                if len(invalid_seasons) > 0:
                    if len(invalid_seasons) == 1:
                        print('\nSeason {} does not exist!'.format(invalid_seasons[0]))
                        raise NameError
                    else:
                        statement = 'Seasons '
                        for i in invalid_seasons:
                            statement += str(i) + " "
                        print("\n" + statement + 'do not exist!')
                        raise NameError
                elif len(user_input) > len(self.full_season_info.keys()) - 1:
                    print('\nYou can not remove all the seasons')
                    user_input = input("> ")
                elif len(user_input) == len(self.full_season_info.keys()) - 1:
                    print("It would be easier for you, if you could use the 'precise' command next time")
                    break
                else:
                    break

            except ValueError:
                print("\nPlease, enter a valid season input")
                print('Ex: 2 and 4 | Ex: 1, 3')
                user_input = input("> ")

            except NameError:
                print('Please, enter a valid season number')
                user_input = input('> ')

        return user_input

    def episode_quantity_decider(self):
        """Forces the user choose the episode_quantity"""
        print("\nHow many episodes would you like to watch today, Sir?")
        self.episode_quantity = self.input_corrector(input('> '))
        self.quantity_force()

    def quantity_force(self):
        """Forces the user watch a maximum of 3 episodes"""
        while self.episode_quantity > 3:
            print('\nNo way! You should actually watch a movie then!')
            print('Yes, right. I am programmed to not to let you watch more than 3 episodes')
            print('So, again: How many episodes would you like to watch today, Sir?')
            self.episode_quantity = self.input_corrector(input('> '))

    def removal_decider(self):
        """Asks if the user would like to remove any season from randomization process"""
        self.removal = []
        print('\nAre there any seasons that you do not watch from?')
        print("Yes : 1  No : 0")
        binary = self.input_corrector(input('> '), binary=True)
        if binary:
            print('\nWhich season(s)? Enter the seasons for removal!')
            print('Ex: 2 and 4 or Ex: 1, 3')
            self.removal = self.removal_input_corrector(input('> '))

    def randomization_preprocessing(self):
        """Copies the full season data, deletes the watched episodes (written in
        history.txt), removes the seasons upon request, copies all the rest
        of the episodes in a list for random selection"""
        copied_data: dict = deepcopy(self.full_season_info)
        for value in self.watched.values():
            try:
                del copied_data[value[0]][value[1]]
            except KeyError:
                pass

        for elem in self.removal:
            del copied_data[elem]

        all_episodes = []
        for season in copied_data.keys():
            for episode in copied_data[season].values():
                all_episodes.append(episode)

        return copied_data, all_episodes

    def pure_chance(self):
        """Randomly chooses episodes and stores it in self.duals"""
        copied_data, all_episodes = self.randomization_preprocessing()
        random_episodes = random.sample(all_episodes, self.episode_quantity)
        for index, elem in enumerate(random_episodes):
            self.duals[index] = get_key(elem, self.full_season_info)

    def episode_statements(self):
        """Prints out the recommended episodes"""
        print('\n        --- Recommended Episodes ---')
        for index, elem in enumerate(self.duals.values(), start=1):
            print("\nChosen episode {}: '{}' from season {}".format(
                index,
                self.full_season_info[elem[0]][elem[1]],
                elem[0]
            ))

    def forth_and_back(self):
        """If desired, directs the user to first recommended episode"""
        print("\nWould you like to start watching the first recommended episode?")
        print("Yes:1  No:0")
        start_watching = self.input_corrector(input("> "), binary=True)
        if start_watching:
            self.direct_website(self.episode_quantity)
            self.duals = dict()
        else:
            print("\nSounds good!")

    def watch(self, quantity: int = 0, full_random: int = 0):
        """Main method to run the class
        @param quantity: number of episodes to watch
        @param full_random: indicator of choosing from all existing episodes or not.
                            Implemented for the 'go' command"""
        self.duals = dict()

        if quantity:
            self.episode_quantity = quantity
            self.quantity_force()
        else:
            self.episode_quantity_decider()

        self.pure_chance()

        if full_random:  # if the command is 'go'
            self.direct_website(self.episode_quantity)
            self.duals = dict()
        else:
            self.removal_decider()
            print(text('\nLoading', 2), end="\r")
            print("Finally, here you go:")
            self.episode_statements()
            self.forth_and_back()


class Visualize(Watch):
    """Implemented for the display command"""

    def __init__(self, data):
        super().__init__(data)

    def display(self, argument):
        if argument == 'all':
            for season_number in self.full_season_info.keys():
                print('\n\t--- Season {} Episodes ---'.format(season_number))
                for index, value in enumerate(self.full_season_info[season_number].items()):
                    if index == 0:
                        print('\n{} :-> {}'.format(value[0], value[1]))
                    else:
                        print('{} :-> {}'.format(value[0], value[1]))
        else:
            print('\n--- Season {} Episodes ---'.format(argument))
            for index, value in enumerate(self.full_season_info[argument].items()):
                if index == 0:
                    print('\n{} :-> {}'.format(value[0], value[1]))
                else:
                    print('{} :-> {}'.format(value[0], value[1]))


class Precise(Visualize):
    """Implemented for the precise command"""

    def __init__(self, data):
        super().__init__(data)
        self.season_input = 0
        self.episode_quantity = 1

    def specific_episode(self):
        """Makes the user to choose a specific episode"""
        print("\nWhich season do you have in mind today, Sir?")
        self.season_input = self.input_corrector(input("> "), season=True)
        print("\nWould your prefer to see the episodes in season " + str(self.season_input) + "?")
        print("Yes : 1  No : 0")
        show = self.input_corrector(input("> "), binary=True)
        self.duals = {0: [self.season_input, self.episode_decider(show)]}

    def episode_decider(self, show):
        """
        Decides the episode to be watched
        @param show: Binary -> If the user would like to see
                    the all episodes exist for the given season
        @return: the episode number
        """
        if show:
            self.display(self.season_input)
            print("\nWhich episode looks desirable?")
            episode_input = self.input_corrector(input("> "), selected_season=self.season_input, episode=True)
        else:
            print("\nWhat is the desired episode?")
            episode_input = self.input_corrector(input("> "), selected_season=self.season_input, episode=True)
        return episode_input

    def absolute_precision(self, season_number, episode_number):
        """
        Directs the user to the website. Parameters are validated.
        @param season_number: given season number by the user
        @param episode_number: given episode number by the user
        """
        self.duals = {0: [season_number, episode_number]}
        self.direct_website(1)

    def precise(self):
        """Main method to run the class if no arguments are given next to precise command"""
        self.specific_episode()
        self.direct_website(1)
