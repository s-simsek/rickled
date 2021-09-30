def helper():
    print('\n=== Welcome to a Rick and Morty Episode Selector ===')

    print("\n Please provide all your season and episode inputs as numbers")

    print("\n---- Available Commands ----")

    print("\n'precise': Select a season to watch a single episode")
    print("\tThis command can get two additional arguments to indicate a specific episode")
    print("\tEx: 'precise 2 3' will immediately open episode 3 from season 2\n")

    print("'watch': Watch random episode(s) from random season(s)")
    print('\tThis command can take an additional argument to indicate the number of episodes to watch')
    print("\tEx:'watch 3' means that the user wants to watch 3 episodes\n")

    print("'go': Randomly chooses one episode out of all existing episodes")

    print("'switch': Switch the rick and morty episode provider\n")

    print("'display': Takes a second argument -> integer, or the string 'all'")
    print("\tDisplays the episode from given season")
    print("\tIf second argument == 'all', displays all existing episodes\n")

    print("'history': Takes a second argument -> integer, or the string 'all'")
    print("\tDisplays a number of (provided by second argument) previously watched episodes")
    print("\tIf the second argument == 'all', all the history will be shown.\n")

    print("'delete': (DANGEROUS) Takes a second argument -> integer, or the string 'all'")
    print("\tDeletes a number of entries (provided by second argument) from history")
    print("\tIf the provided integer is greater than the length of the history, an exception is raised")
    print("\tIf the second argument == 'all', all the history will be deleted\n")

    print("'clear': Clears the page\n")

    print("'exit': Closes the program")

    print("\nYou can type 'exit' and 'clear' in any input section.")
    print("However, if you are in the middle of the other commands' workflow, typing ")
    print("any other command will not work. You need to get to the end of the commands' process")
    print("in order to use any other command.")
