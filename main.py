import sys
import subprocess as sp
from watch import Precise
from helper import helper
from episode_scrapper import *


class Commands(Precise):
    user_input: list

    def __init__(self):
        episode_info = EpisodeData()
        self.data = episode_info.episode_data
        super().__init__(self.data)

    def command_corrector(self, user_input: str) -> list:
        """Forces the user to provide a valid command"""

        available_commands = ['watch', 'precise', 'help', 'history', 'display',
                              'delete', 'switch', 'clear', 'exit', 'go']
        # TODO: Implement the update command
        while True:
            try:
                command_input = user_input.split(" ")
                first_arg = command_input[0]

                if first_arg not in available_commands:
                    raise EnvironmentError

                elif first_arg == 'precise' and len(command_input) > 1:
                    if len(command_input) == 3:
                        season_number = int(command_input[1])
                        episode_number = int(command_input[2])
                        if season_number not in self.data.keys():
                            print('\nPlease, enter a valid season number')
                            user_input = input('> ')
                        elif episode_number not in self.data[season_number].keys():
                            print('\nPlease, enter a valid episode a number')
                            user_input = input('> ')
                        else:
                            return [first_arg, season_number, episode_number]
                    else:
                        print('\nprecise command either takes 2 or no additional arguments')
                        user_input = input('> ')

                elif first_arg == 'watch' and len(command_input) == 2:
                    second_arg = int(command_input[1])
                    if second_arg < 0:
                        raise ValueError
                    else:
                        return [first_arg, second_arg]

                elif (first_arg == 'history' or first_arg == 'delete' or first_arg == 'display') \
                        and len(command_input) == 1:
                    print('\n{} command needs a second argument'.format(first_arg))
                    user_input = input('> ')

                elif first_arg == 'display':
                    if len(command_input) == 2:
                        second_arg = command_input[1]
                        if second_arg == 'all':
                            return [first_arg, second_arg]
                        elif int(second_arg) and int(second_arg) in self.data.keys():
                            return [first_arg, int(second_arg)]
                        else:
                            raise ValueError

                elif first_arg == 'delete' or first_arg == 'history':
                    if len(command_input) == 2:
                        second_arg = command_input[1]
                        if second_arg == 'all':
                            return [first_arg, second_arg]
                        elif int(second_arg):
                            return [first_arg, int(second_arg)]
                        else:
                            raise ValueError

                elif first_arg == 'go':
                    if len(command_input) > 1:
                        print("'go' command does not take any additional arguments")
                        user_input = input('> ')
                    else:
                        return [first_arg]

                elif len(command_input) > 1:
                    raise EnvironmentError

                else:
                    return [first_arg]

            except EnvironmentError:
                print('\nPlease, enter a valid command')
                user_input = input('> ')

            except ValueError:
                print('\nPlease, enter a valid additional argument')
                user_input = input('> ')

    def engine(self):
        """Main method to run the class"""
        while True:
            self.user_input = self.command_corrector(input('> '))
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
            elif self.user_input[0] == 'clear':
                sp.call('cls', shell=True)
            elif self.user_input[0] == 'exit':
                sys.exit()


if __name__ == "__main__":
    initiation = Commands()
    sp.call('cls', shell=True)
    print('\nWhat would you like me to do, Sir?')
    print('You can type "help"')
    initiation.engine()
