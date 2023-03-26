# pokemon-match

This script creates a PyQt6 application called "Pokemon Fight Club" that allows users to randomly pair and select the winners of Pokemon battles in a knockout tournament style. It reads a list of Pokemon names from a file named "pokemons.txt" and creates a table with pairs of battling Pokemon for each round. The user can click on the winner of each match, and the app will generate the next round based on the winners of the previous round.

Key components of the script:

Import necessary libraries: sys, random, math, and PyQt6-related classes.
PokemonFightClub class is defined, inheriting from QMainWindow.
The __init__ method initializes the application, reads the list of Pokemon from the file, and sets up the initial window.
The init_tabs method sets up the tabs for the application, and init_tab1 method initializes the first tab with the first round of matches.
ordinal method is a utility function that returns an ordinal number as a string (e.g., 1st, 2nd, 3rd).
create_bottom_buttons method creates the buttons for drawing matches, going to the next draw, and resetting the draw.
generate_matches method takes the current round number as input and generates the matches for that round, either from the original Pokemon list or the list of winners from the previous round.
select_winner method is called when a user clicks on a Pokemon name in a match; it sets the winner and updates the table's background color accordingly.
reset_draw method resets the entire draw, removing all tabs except the first one and regenerating the first round.
