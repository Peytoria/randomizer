import random
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QSpinBox,
                            QListWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class RandomizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MTG Jumpstart Randomizer")
        self.setMinimumSize(400, 500)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("MTG Jumpstart Randomizer")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Player count input
        player_count_layout = QHBoxLayout()
        player_count_label = QLabel("Number of Players:")
        self.player_count_spin = QSpinBox()
        self.player_count_spin.setMinimum(2)
        self.player_count_spin.setMaximum(8)
        self.player_count_spin.setValue(4)
        player_count_layout.addWidget(player_count_label)
        player_count_layout.addWidget(self.player_count_spin)
        layout.addLayout(player_count_layout)
        
        # Randomize button
        self.randomize_btn = QPushButton("Randomize Pick Order")
        self.randomize_btn.clicked.connect(self.randomize_order)
        layout.addWidget(self.randomize_btn)
        
        # Results list
        self.results_list = QListWidget()
        layout.addWidget(self.results_list)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Set style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 14px;
            }
            QSpinBox {
                padding: 4px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
        """)

    def randomize_order(self):
        num_players = self.player_count_spin.value()
        players = list(range(1, num_players + 1))
        random.shuffle(players)
        
        self.results_list.clear()
        for i, player in enumerate(players, 1):
            self.results_list.addItem(f"Pick {i}: Player {player}")
        
        self.status_label.setText("Pick order has been randomized!") 