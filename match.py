import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, \
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, \
    QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class PokemonFightClub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.matches_table = QTableWidget(0, 2)  # Initially empty table
        self.setWindowTitle("Pokemon Fight Club")

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        self.init_tabs()

        self.show()
        self.winners = []

    def init_tabs(self):
        self.init_tab1()
        self.init_tab2()
        self.init_tab3()

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

        # Set header section resize mode
        self.matches_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set row number alignment
        self.matches_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        # Remove custom borders
        self.matches_table.setStyleSheet("")

        layout1.addWidget(self.matches_table)

        layout_buttons = QHBoxLayout()
        draw_button = QPushButton('Draw')
        draw_button.clicked.connect(self.generate_matches)
        layout_buttons.addWidget(draw_button)

        next_draw_button = QPushButton('Next Draw')
        next_draw_button.clicked.connect(self.next_draw)
        layout_buttons.addWidget(next_draw_button)
        layout1.addLayout(layout_buttons)

        self.tabs.addTab(tab1, "First Round")

    def generate_matches(self):
        with open('pokemons.txt', 'r') as f:
            pokemons = f.read().splitlines()

        random.shuffle(pokemons)

        num_matches = len(pokemons) // 2

        self.matches_table.setRowCount(num_matches)
        self.winners = []
        for i in range(num_matches):
            p1 = pokemons[2 * i]
            p2 = pokemons[2 * i + 1]

            item_p1 = QTableWidgetItem(p1)
            item_p1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_p1.setFlags(item_p1.flags() | Qt.ItemFlag.ItemIsSelectable)
            item_p1.setBackground(Qt.GlobalColor.white)
            self.matches_table.setItem(i, 0, item_p1)

            item_p2 = QTableWidgetItem(p2)
            item_p2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_p2.setFlags(item_p2.flags() | Qt.ItemFlag.ItemIsSelectable)
            item_p2.setBackground(Qt.GlobalColor.white)
            self.matches_table.setItem(i, 1, item_p2)

    def select_winner(self, row, column):
        winner = self.matches_table.item(row, column).text()
        self.winners.append(winner)

        for col in range(2):
            item = self.matches_table.item(row, col)
            if col == column:
                item.setBackground(Qt.GlobalColor.green)
            else:
                item.setBackground(Qt.GlobalColor.white)

    def init_tab2(self):
        tab2 = QWidget()
        layout2 = QVBoxLayout(tab2)

        # Set header font to bold
        font = QFont()
        font.setBold(True)
        self.matches_table.horizontalHeader().setFont(font)

        self.round2_table = QTableWidget(0, 2)
        self.round2_table.setHorizontalHeaderLabels(['POKEMON 1', 'POKEMON 2'])
        self.round2_table.horizontalHeader().setFont(font)
        self.round2_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.round2_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.round2_table.cellClicked.connect(self.select_winner)
        layout2.addWidget(self.round2_table)

        self.tabs.addTab(tab2, "2nd Round")

    def init_tab3(self):
        tab3 = QWidget()
        self.tabs.addTab(tab3, "3rd Round")

    def next_draw(self):
        if not self.winners:
            return

        random.shuffle(self.winners)

        num_matches = len(self.winners) // 2

        self.round2_table.setRowCount(num_matches)
        for i in range(num_matches):
            p1 = self.winners[2 * i]
            p2 = self.winners[2 * i + 1]

            item_p1 = QTableWidgetItem(p1)
            item_p1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_p1.setFlags(item_p1.flags() | Qt.ItemFlag.ItemIsSelectable)
            item_p1.setBackground(Qt.GlobalColor.white)
            self.round2_table.setItem(i, 0, item_p1)

            item_p2 = QTableWidgetItem(p2)
            item_p2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_p2.setFlags(item_p2.flags() | Qt.ItemFlag.ItemIsSelectable)
            item_p2.setBackground(Qt.GlobalColor.white)
            self.round2_table.setItem(i, 1, item_p2)

        self.tabs.setCurrentIndex(1)  # Switch to the "2nd Round" tab


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = PokemonFightClub()
    sys.exit(app.exec())
