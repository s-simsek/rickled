class CommandError(BaseException):
    """Exception raised for invalid command inputs"""

    def __init__(self, command):
        self.command = command
        super(CommandError, self).__init__()
        message = f'{self.command} is not a valid command!'
        print(message)


class ArgumentError(BaseException):
    """Exception raised for invalid command inputs"""

    def __init__(self, command):
        super(ArgumentError, self).__init__()
        message = f"'{command}' command got extra unnecessary arguments"
        print(message)


def command_corrector(data, user_input: str) -> list:
    """
    Forces the user to provide a valid command
    @param data: 2d episode dictionary data
    @param user_input: user input from the command prompt
    @return: list -> first element is the main command
                     other elements, if any, are the additional arguments in order
    """

    available_commands = ['watch', 'precise', 'help', 'history', 'display',
                          'delete', 'switch', 'clear', 'exit', 'go', 'update']
    while True:
        try:
            command_input = user_input.split(" ")
            first_arg = command_input[0]

            if first_arg not in available_commands:
                raise CommandError(first_arg)

            elif first_arg == 'precise':
                if len(command_input) == 1:
                    return [first_arg]
                elif len(command_input) == 2:
                    print('\n "precise" command takes no or 2 arguments')
                    user_input = input("> ")
                elif len(command_input) == 3:
                    season_number = int(command_input[1])
                    episode_number = int(command_input[2])
                    if season_number not in data.keys():
                        print('\nPlease, enter a valid season number')
                        user_input = input('> ')
                    elif episode_number not in data[season_number].keys():
                        print('\nPlease, enter a valid episode a number')
                        user_input = input('> ')
                    else:
                        return [first_arg, season_number, episode_number]
                else:
                    raise ArgumentError(first_arg)

            elif first_arg == 'watch':
                if len(command_input) == 1:
                    return [first_arg]
                elif len(command_input) == 2:
                    second_arg = int(command_input[1])
                    if second_arg < 0:
                        raise ValueError
                    else:
                        return [first_arg, second_arg]
                else:
                    raise ArgumentError(first_arg)

            elif (first_arg == 'history' or first_arg == 'delete' or first_arg == 'display') \
                    and len(command_input) == 1:
                print(f'\n{first_arg} command needs a second argument')
                user_input = input('> ')

            elif first_arg == 'display':
                if len(command_input) == 2:
                    second_arg = command_input[1]
                    if second_arg == 'all':
                        return [first_arg, second_arg]
                    elif int(second_arg) and int(second_arg) in data.keys():
                        return [first_arg, int(second_arg)]
                    else:
                        raise ValueError
                else:
                    raise ArgumentError(first_arg)

            elif first_arg == 'delete' or first_arg == 'history':
                if len(command_input) == 2:
                    second_arg = command_input[1]
                    if second_arg == 'all':
                        return [first_arg, second_arg]
                    elif int(second_arg):
                        return [first_arg, int(second_arg)]
                    else:
                        raise ValueError
                else:
                    raise ArgumentError(first_arg)

            elif first_arg == 'go' or first_arg == 'update':
                if len(command_input) > 1:
                    raise ArgumentError(first_arg)
                else:
                    return [first_arg]

            else:  # The first arg can be: precise, watch
                return [first_arg]

        except ArgumentError:
            user_input = input('> ')
        except CommandError:
            user_input = input('> ')
        except ValueError:
            print('\nPlease, enter a valid integer additional argument(s)')
            user_input = input('> ')
