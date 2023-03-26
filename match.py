import sys
import random
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class PokemonFightClub(QMainWindow):
    def __init__(self):
        super().__init__()
        with open('pokemons.txt', 'r') as f:
            pokemons = f.read().splitlines()
        self.initial_participants = len(pokemons)
        self.round_done = {0: False}  # Add a dictionary to keep track of round completion status
        self.matches_table = QTableWidget(0, 2)  # Initially empty table
        self.setWindowTitle("Pokemon Fight Club")
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.init_tabs()
        self.show()
        self.winners = []  # Add a new list for the 1st round winners
        self.round_done = {0: False}

    def init_tabs(self):
        self.init_tab1()

    def init_tab1(self):
        tab1 = QWidget()
        layout1 = QVBoxLayout(tab1)

        self.matches_table = QTableWidget(0, 2)  # Initially empty table
        self.matches_table.setHorizontalHeaderLabels(['POKEMON 1', 'POKEMON 2'])
        self.matches_table.cellClicked.connect(self.select_winner)

        # Set header font to bold
        font = QFont()
        font.setBold(True)
        self.matches_table.horizontalHeader().setFont(font)

        self.matches_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set row number alignment
        self.matches_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        # Remove custom borders
        self.matches_table.setStyleSheet("")

        layout1.addWidget(self.matches_table)
        layout_buttons = self.create_bottom_buttons()
        layout1.addLayout(layout_buttons)
        self.tabs.addTab(tab1, "1st Round")

    @staticmethod
    def ordinal(n):
        suffix = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']
        if 10 <= n % 100 <= 20:
            suffix_index = 0
        else:
            suffix_index = n % 10

        return str(n) + suffix[suffix_index]

    def create_bottom_buttons(self):
        layout_buttons = QHBoxLayout()
        draw_button = QPushButton('Draw')
        draw_button.clicked.connect(self.generate_matches)
        layout_buttons.addWidget(draw_button)

        next_draw_button = QPushButton('Next Draw')
        next_draw_button.clicked.connect(self.next_draw)
        layout_buttons.addWidget(next_draw_button)

        reset_draw_button = QPushButton('Reset Draw')
        reset_draw_button.clicked.connect(self.reset_draw)
        layout_buttons.addWidget(reset_draw_button)

        return layout_buttons

    def generate_matches(self, current_round):
        if self.round_done[current_round]:
            return

        if current_round == 0:
            with open('pokemons.txt', 'r') as f:
                pokemons = f.read().splitlines()
        else:
            pokemons = self.winners

        random.shuffle(pokemons)

        num_matches = len(pokemons) // 2
        matches_table = self.matches_table if current_round == 0 else self.tabs.widget(current_round).findChild(QTableWidget)

        matches_table.setRowCount(num_matches)
        self.winners = []
        for i in range(num_matches):
            p1 = pokemons[2 * i]
            p2 = pokemons[2 * i + 1]

            item_p1 = QTableWidgetItem(p1)
            item_p1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_p1.setFlags(item_p1.flags() | Qt.ItemFlag.ItemIsSelectable)
            item_p1.setBackground(Qt.GlobalColor.white)
            matches_table.setItem(i, 0, item_p1)

            item_p2 = QTableWidgetItem(p2)
            item_p2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_p2.setFlags(item_p2.flags() | Qt.ItemFlag.ItemIsSelectable)
            item_p2.setBackground(Qt.GlobalColor.white)
            matches_table.setItem(i, 1, item_p2)

        self.round_done[current_round] = True

    def select_winner(self, row, column):
        matches_table = self.tabs.currentWidget().findChild(QTableWidget)

        winner = matches_table.item(row, column).text()
        self.winners.append(winner)

        for col in range(2):
            item = matches_table.item(row, col)
            if col == column:
                item.setBackground(Qt.GlobalColor.green)
            else:
                item.setBackground(Qt.GlobalColor.white)

        competitors_left = matches_table.rowCount() * 2
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
        if not self.winners:
            return

        current_round = self.tabs.currentIndex()
        next_round = current_round + 1

        if self.round_done.get(next_round, False):
            return

        if next_round not in self.round_done:
            self.round_done[next_round] = False

        if len(self.winners) == 1:
            # Winner tab
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

        next_round_matches_table = QTableWidget(0, 2)
        next_round_matches_table.setHorizontalHeaderLabels(['POKEMON 1', 'POKEMON 2'])
        next_round_matches_table.cellClicked.connect(self.select_winner)
        next_round_matches_table.horizontalHeader().setFont(font)
        next_round_matches_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        next_round_matches_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        next_round_layout.addWidget(next_round_matches_table)
        next_round_layout.addLayout(self.create_bottom_buttons())

        self.tabs.addTab(next_round_tab, self.round_name(next_round))  # Moved this line down here
        self.tabs.setCurrentIndex(next_round)  # Added this line to switch to the new tab

        self.generate_matches(next_round)

    def round_name(self, round_number):
        total_rounds = math.ceil(math.log2(self.initial_participants))

        if round_number == total_rounds - 2:
            return "Final"
        elif round_number == total_rounds - 3:
            return "Semi Final"
        elif round_number == total_rounds - 4:
            return "Quarter Final"
        else:
            return f"{self.ordinal(round_number + 1)} Round"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = PokemonFightClub()
    sys.exit(app.exec())
