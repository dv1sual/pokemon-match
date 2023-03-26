Pokemon Fight Club

This is a simple Python application that simulates a Pokemon tournament, randomly drawing matchups and allowing the user to select winners. The application uses PyQt6 for the graphical user interface.

Features

1. Load a list of Pokemon names from a text file.
2. Randomly generate matchups for each round.
3. Select winners for each matchup.
4. Progress through the tournament until a winner is declared.
5. Reset the tournament and start a new one.
6. Navigate between the rounds with tabbed interface.

Installation

To run the Pokemon Fight Club application, you will need Python 3.6 or higher and the PyQt6 library installed. You can install PyQt6 using pip:
    -pip install PyQt6

Usage

1. Make sure you have a file named pokemons.txt in the same directory as the script. This file should contain the names of the Pokemon participants, one per line.
2. Run the main.py script using Python:
    -python main.py
3. The application will display the "1st Round" tab with an initially empty table.
4. Click the "Draw" button to generate the first-round matchups.
5. Click on a cell in the table to select a winner for each matchup.
6. Once all winners are selected, click the "Next Draw" button to move on to the next round.
7. Continue selecting winners and progressing through the rounds until a winner is declared in the final round. The application will display a message box announcing the winner.
8. To start a new tournament, click the "Reset Draw" button. This will reset the application, clearing all rounds and winners.
9. You can navigate between the different rounds by clicking the tabs at the top of the application window.

Customization

To use a different set of participants, edit the pokemons.txt file and add or remove the names as needed. The application will automatically adjust the number of rounds and matchups based on the number of participants provided.

License

This project is released under the MIT License. See the LICENSE file for more information.

Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements, bug fixes, or new features you'd like to add.
