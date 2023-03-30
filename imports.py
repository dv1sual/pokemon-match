import os
import sys
import random
import math
import requests
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QLabel, QDialog, QProgressBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPixmap, QBrush, QPalette
from io import BytesIO
import pyttsx3
import threading
import queue
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
