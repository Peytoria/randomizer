import sys
import json
import os
import random
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QPushButton, QLineEdit, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt, QSettings

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/names.json")
ORG_NAME = "JumpstartTools"
APP_NAME = "JumpstartRandomizer"

def load_names():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_names(names):
    with open(DATA_FILE, "w") as f:
        json.dump(names, f)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jumpstart Randomizer")
        self.settings = QSettings(ORG_NAME, APP_NAME)
        self.names = sorted(set(load_names()))

        self.layout = QVBoxLayout()

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter a name")
        self.input_line.returnPressed.connect(self.add_name)
        self.layout.addWidget(self.input_line)

        button_row = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.remove_button = QPushButton("Remove")
        self.clear_button = QPushButton("Clear All")
        self.shuffle_button = QPushButton("Shuffle")
        button_row.addWidget(self.add_button)
        button_row.addWidget(self.remove_button)
        button_row.addWidget(self.clear_button)
        button_row.addWidget(self.shuffle_button)
        self.layout.addLayout(button_row)

        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.layout.addWidget(self.dark_mode_checkbox)

        self.list_widget = QListWidget()
        self.list_widget.addItems(self.names)
        self.layout.addWidget(self.list_widget)

        self.output_label = QLabel("Shuffled Order: ")
        self.layout.addWidget(self.output_label)

        self.setLayout(self.layout)

        self.add_button.clicked.connect(self.add_name)
        self.remove_button.clicked.connect(self.remove_name)
        self.clear_button.clicked.connect(self.clear_all)
        self.shuffle_button.clicked.connect(self.shuffle_names)
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)

        self.restore_window_state()
        self.input_line.setFocus()

    def add_name(self):
        name = self.input_line.text().strip()
        if name and name not in self.names:
            self.names.append(name)
            self.names = sorted(set(self.names))
            self.refresh_list()
            save_names(self.names)
        self.input_line.clear()
        self.input_line.setFocus()

    def remove_name(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Remove Name", "Select a name to remove.")
            return
        confirm = QMessageBox.question(
            self, "Confirm Removal",
            "Are you sure you want to remove the selected name(s)?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            for item in selected_items:
                self.names.remove(item.text())
                self.list_widget.takeItem(self.list_widget.row(item))
            save_names(self.names)

    def clear_all(self):
        confirm = QMessageBox.question(
            self, "Confirm Clear All",
            "Are you sure you want to clear all names?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.names = []
            self.refresh_list()
            save_names(self.names)

    def shuffle_names(self):
        if not self.names:
            self.output_label.setText("Shuffled Order: (empty)")
            return
        shuffled = self.names[:]
        random.shuffle(shuffled)
        self.output_label.setText(f"Shuffled Order: {', '.join(shuffled)}")
        QMessageBox.information(self, "Shuffle Complete", "Names have been shuffled!")

    def refresh_list(self):
        self.list_widget.clear()
        self.list_widget.addItems(self.names)

    def toggle_dark_mode(self, state):
        if state == Qt.Checked:
            self.setStyleSheet("""
                QWidget {
                    background-color: #121212;
                    color: #f0f0f0;
                }
                QPushButton, QLineEdit, QListWidget {
                    background-color: #2e2e2e;
                    color: #ffffff;
                    border: 1px solid #444;
                }
            """)
        else:
            self.setStyleSheet("")

    def restore_window_state(self):
        size = self.settings.value("window_size")
        pos = self.settings.value("window_pos")
        if size:
            self.resize(size)
        if pos:
            self.move(pos)

    def closeEvent(self, event):
        self.settings.setValue("window_size", self.size())
        self.settings.setValue("window_pos", self.pos())
        event.accept()

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
