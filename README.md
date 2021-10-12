<h2> Rick and Morty Random Episode Thrower </h2>

![](r_m_2.png)


Run main.py to run the program. You can type 'help' on the command screen to see available commands.

---

<h4> Available Commands </h4>

1. `precise`

- Select a season to watch a single episode
- This command can get two additional arguments to indicate a specific episode
- Ex: 'precise 2 3' will immediately open episode 3 from season 2

2. `watch`:
 
- Watch random episode(s) from random season(s)
- This command can take an additional argument to indicate the number of episodes to watch
- Ex: 'watch 3' means that the user wants to watch 3 episodes

3. `go`

- Randomly chooses one episode out of all existing episodes

4. `switch`

- Switch the rick and morty episode provider

5. `display`

- Takes a second argument -> integer, or the string 'all'
- Displays the episode from given season
- If second argument == 'all', displays all existing episodes

6. `history`

- Takes a second argument -> integer, or the string 'all'
- Displays a number of (provided by second argument) previously watched episodes
- If the second argument == 'all', all the history will be shown

7. `delete` [Dangerous]

- Takes a second argument -> integer, or the string 'all'
- Deletes a number of entries (provided by second argument) from history
- If the provided integer is greater than the length of the history, an exception is raised
- If the second argument == 'all', all the history will be deleted

8. `clear`

- Clears the page

9. `exit`

- Closes the program


*Note*:
You can type 'exit' and 'clear' in any input section.
However, if you are in the middle of the other commands' workflow, typing
any other command will not work. You need to get to the end of the commands' process
in order to use any other command.






















