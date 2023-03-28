import sys
import random
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class PokemonBattlesClub(QMainWindow):
    def __init__(self):
        super().__init__()

        # Read the list of Pokémon from the 'Pokémon.txt' file
        with open('pokemons.txt', 'r') as f:
            pokemons = f.read().splitlines()

        # Store the initial number of participants
        self.initial_participants = len(pokemons)

        # Initialize a dictionary to track the completion status of each round
        self.round_done = {0: False}

        # Create an initially empty table for matches
        self.matches_table = QTableWidget(0, 2)

        # Set the window title
        self.setWindowTitle("Pokemon Battles Club")

        # Create a tab widget and set it as the central widget of the main window
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Initialize the tabs
        self.init_tabs()

        # Show the main window
        self.show()

        # Initialize an empty list to store the winners of each round
        self.winners = []

        # Reset the round_done dictionary for the first round
        self.round_done = {0: False}

    def init_tabs(self):
        self.init_tab1()

    def init_tab1(self):
        # Create a QWidget object for the first tab
        tab1 = QWidget()

        # Set a QVBoxLayout as the layout for the first tab
        layout1 = QVBoxLayout(tab1)

        # Initialize an empty QTableWidget for the first round matches
        self.matches_table = QTableWidget(0, 2)

        # Set the header labels for the matches table
        self.matches_table.setHorizontalHeaderLabels(['POKEMON 1', 'POKEMON 2'])

        # Connect the cellClicked signal to the select_winner function
        self.matches_table.cellClicked.connect(self.select_winner)

        # Create a QFont object and set its bold property to True
        font = QFont()
        font.setBold(True)

        # Apply the bold font to the horizontal header of the matches table
        self.matches_table.horizontalHeader().setFont(font)

        # Set the stretch resize mode for the horizontal header of the matches table
        self.matches_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Align the row numbers to the center for the vertical header of the matches table
        self.matches_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        # Remove custom borders from the matches table
        self.matches_table.setStyleSheet("")

        # Add the matches table to the layout of the first tab
        layout1.addWidget(self.matches_table)

        # Create the bottom buttons (Draw, Next Draw, and Reset Draw) and add them to a QHBoxLayout
        layout_buttons = self.create_bottom_buttons()

        # Add the layout containing the bottom buttons to the main layout of the first tab
        layout1.addLayout(layout_buttons)

        # Add the first tab (tab1) with the layout (layout1) to the tabs (QTabWidget) and set its label as "1st Round"
        self.tabs.addTab(tab1, "1st Round")

    def create_bottom_buttons(self):
        # Create a horizontal layout to store the buttons
        layout_buttons = QHBoxLayout()

        # Create the 'Draw' button and connect its clicked signal to the 'generate_matches' method
        draw_button = QPushButton('Draw')
        draw_button.clicked.connect(self.generate_matches)

        # Add the 'Draw' button to the horizontal layout
        layout_buttons.addWidget(draw_button)

        # Create the 'Next Draw' button and connect its clicked signal to the 'next_draw' method
        next_draw_button = QPushButton('Next Draw')
        next_draw_button.clicked.connect(self.next_draw)

        # Add the 'Next Draw' button to the horizontal layout
        layout_buttons.addWidget(next_draw_button)

        # Create the 'Reset Draw' button and connect its clicked signal to the 'reset_draw' method
        reset_draw_button = QPushButton('Reset Draw')
        reset_draw_button.clicked.connect(self.reset_draw)

        # Add the 'Reset Draw' button to the horizontal layout
        layout_buttons.addWidget(reset_draw_button)

        # Return the horizontal layout containing the bottom buttons
        return layout_buttons

    def generate_matches(self, current_round):
        # Return if the current round is already done
        if self.round_done[current_round]:
            return

        # If it's the first round, read the list of Pokémon from the file
        if current_round == 0:
            with open('pokemons.txt', 'r') as f:
                pokemons = f.read().splitlines()
        else:
            # For subsequent rounds, use the winners from the previous round
            pokemons = self.winners

        # Shuffle the Pokémon randomly
        random.shuffle(pokemons)

        # Calculate the number of matches for the current round
        num_matches = len(pokemons) // 2

        # Get the appropriate matches table for the current round
        matches_table = self.matches_table if current_round == 0 else self.tabs.widget(current_round).findChild(QTableWidget)

        # Set the number of rows in the matches table
        matches_table.setRowCount(num_matches)

        # Clear the winners list for the current round
        self.winners = []

        # Populate the matches table with Pokémon
        for i in range(num_matches):
            p1 = pokemons[2 * i]
            p2 = pokemons[2 * i + 1]

            # Create and configure QTableWidgetItem for the first Pokémon (p1)
            item_p1 = QTableWidgetItem(p1)
            item_p1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_p1.setFlags(item_p1.flags() | Qt.ItemFlag.ItemIsSelectable)
            item_p1.setBackground(Qt.GlobalColor.white)

            # Add the QTableWidgetItem to the matches table
            matches_table.setItem(i, 0, item_p1)

            # Create and configure QTableWidgetItem for the second Pokémon (p2)
            item_p2 = QTableWidgetItem(p2)
            item_p2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_p2.setFlags(item_p2.flags() | Qt.ItemFlag.ItemIsSelectable)
            item_p2.setBackground(Qt.GlobalColor.white)

            # Add the QTableWidgetItem to the matches table
            matches_table.setItem(i, 1, item_p2)

        # Mark the current round as done
        self.round_done[current_round] = True

    def select_winner(self, row, column):
        # Find the matches table in the current tab
        matches_table = self.tabs.currentWidget().findChild(QTableWidget)

        # Get the winner's name from the selected table cell
        winner = matches_table.item(row, column).text()

        # Add the winner to the winners list
        self.winners.append(winner)

        # Update the cell background colors to indicate the winner
        for col in range(2):
            item = matches_table.item(row, col)
            if col == column:
                # Set the winner's cell background color to Pokémon Yellow
                item.setBackground(QColor("#FFCC00"))
            else:
                # Set the loser's cell background color to white
                item.setBackground(Qt.GlobalColor.white)

        # Calculate the remaining competitors in the current round
        competitors_left = matches_table.rowCount() * 2

        # If only one competitor is left, display the winner's name in a message box
        if competitors_left == 2 and len(self.winners) == 1:
            msg = QMessageBox()
            msg.setWindowTitle("Winner")
            msg.setText(f"I Choose You! The winner is {winner}.")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def reset_draw(self):
        # Remove all tabs except the first one
        while self.tabs.count() > 1:
            self.tabs.removeTab(self.tabs.count() - 1)

        # Clear the table and the winners list
        self.matches_table.setRowCount(0)
        self.winners = []

        # Reset the round_done dictionary
        self.round_done = {0: False}

    def next_draw(self):
        # If there are no winners, return
        if not self.winners:
            return

        # Get the current round and calculate the next round
        current_round = self.tabs.currentIndex()
        next_round = current_round + 1

        # If the next round is already done, return
        if self.round_done.get(next_round, False):
            return

        # Initialize the round_done status for the next round if not already set
        if next_round not in self.round_done:
            self.round_done[next_round] = False

        # If there's only one winner left, create a "Winner" tab
        if len(self.winners) == 1:
            winner_tab = QWidget()
            winner_layout = QVBoxLayout(winner_tab)
            winner_label = QLabel(f"Winner: {self.winners[0]}")
            winner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            winner_layout.addWidget(winner_label)

            reset_winner_button = QPushButton('Reset Draw')
            reset_winner_button.clicked.connect(self.reset_draw)
            winner_layout.addWidget(reset_winner_button)

            self.tabs.addTab(winner_tab, "Winner")
            self.tabs.setCurrentIndex(next_round)
            self.round_done[next_round] = True
            return

        # Create a new tab for the next round
        next_round_tab = QWidget()
        next_round_layout = QVBoxLayout(next_round_tab)

        font = QFont()
        font.setBold(True)

        # Create and configure the matches table for the next round
        next_round_matches_table = QTableWidget(0, 2)
        next_round_matches_table.setHorizontalHeaderLabels(['POKEMON 1', 'POKEMON 2'])
        next_round_matches_table.cellClicked.connect(self.select_winner)
        next_round_matches_table.horizontalHeader().setFont(font)
        next_round_matches_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        next_round_matches_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add the next round matches table to the layout
        next_round_layout.addWidget(next_round_matches_table)
        # Add the bottom buttons to the layout
        next_round_layout.addLayout(self.create_bottom_buttons())

        # Add the new tab for the next round and set the current index to it
        self.tabs.addTab(next_round_tab, self.round_name(next_round))  # Moved this line down here
        self.tabs.setCurrentIndex(next_round)  # Added this line to switch to the new tab

        # Generate matches for the next round
        self.generate_matches(next_round)

    def round_name(self, round_number):
        # Calculate the total number of rounds in the tournament
        total_rounds = math.ceil(math.log2(self.initial_participants))

        # Determine the name of the current round based on its position
        if round_number == total_rounds - 2:
            return "Final"
        elif round_number == total_rounds - 3:
            return "Semi Final"
        elif round_number == total_rounds - 4:
            return "Quarter Final"
        else:
            # For other rounds, return the ordinal representation of the round number
            return f"{self.ordinal(round_number + 1)} Round"

    @staticmethod
    def ordinal(n):
        # Define a list of suffixes for ordinal numbers
        suffix = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']

        # Determine the appropriate suffix based on the given number
        # If the number is between 10 and 20 (inclusive), use the 'th' suffix
        if 10 <= n % 100 <= 20:
            suffix_index = 0
        else:
            # If the number is not between 10 and 20, use the last digit to determine the suffix
            suffix_index = n % 10

        # Combine the number and the appropriate suffix, then return the result
        return str(n) + suffix[suffix_index]


if __name__ == "__main__":
    # Create a QApplication instance for managing the application's control flow
    app = QApplication(sys.argv)

    # Set the custom style sheet for the application
    with open("stylesheet.qss", "r") as file:
        app.setStyleSheet(file.read())

    # Instantiate the main window for the PokemonBattlesClub application
    mainWin = PokemonBattlesClub()

    # Start the application's event loop and block until it returns
    # This will keep the application running and processing events until it's closed
    sys.exit(app.exec())
