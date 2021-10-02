import subprocess as sp
from commands import Precise
from helper import helper
from episode_scrapper import *
from command_corrector import *


class Commands(Precise):
    user_input: list

    def __init__(self):
        episode_info = EpisodeData()
        self.data = episode_info.episode_data
        super().__init__(self.data)

    def engine(self):
        """Main method to run the class"""
        print('\nWhat would you like me to do, Sir?')
        print('You can type "help"')
        while True:
            self.user_input = command_corrector(self.data, input('> '))
            self.full_season_info = self.data.copy()
            if self.user_input[0] == 'watch':
                if len(self.user_input) == 1:
                    self.watch()
                else:
                    episode_quantity = self.user_input[1]
                    self.watch(quantity=episode_quantity)
            elif self.user_input[0] == 'precise':
                if len(self.user_input) == 1:
                    self.precise()
                else:
                    season_number = self.user_input[1]
                    episode_number = self.user_input[2]
                    self.absolute_precision(season_number, episode_number)
            elif self.user_input[0] == 'go':
                self.watch(quantity=1, full_random=1)
            elif self.user_input[0] == 'help':
                helper()
            elif self.user_input[0] == 'history':
                self.look_back(self.user_input[1])
            elif self.user_input[0] == 'display':
                self.display(self.user_input[1])
            elif self.user_input[0] == 'delete':
                self.delete_record(self.user_input[1])
            elif self.user_input[0] == 'switch':
                self.switch()
            elif self.user_input[0] == 'update':
                EpisodeData().update()
                time.sleep(1)
                sp.call('cls', shell=True)
            elif self.user_input[0] == 'clear':
                sp.call('cls', shell=True)
            elif self.user_input[0] == 'exit':
                sys.exit()


if __name__ == "__main__":
    initiation = Commands()
    sp.call('cls', shell=True)
    initiation.engine()
