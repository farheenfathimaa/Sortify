import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QFileDialog, QListWidget, QLabel, QWidget, QComboBox, QSpinBox
)
from PyQt5.QtCore import QDateTime

class FileOrganizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 600, 500)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # UI Elements
        self.file_list = QListWidget(self)
        self.layout.addWidget(QLabel("Selected Files:"))
        self.layout.addWidget(self.file_list)

        self.select_button = QPushButton("Select Files")
        self.select_button.clicked.connect(self.select_files)
        self.layout.addWidget(self.select_button)

        # Sorting criteria
        self.layout.addWidget(QLabel("Sort by:"))
        self.sort_criteria = QComboBox()
        self.sort_criteria.addItems(["Date", "Size", "Custom Category"])
        self.layout.addWidget(self.sort_criteria)

        # Number of folders
        self.layout.addWidget(QLabel("Number of Folders:"))
        self.folder_count = QSpinBox()
        self.folder_count.setMinimum(1)
        self.folder_count.setValue(1)
        self.layout.addWidget(self.folder_count)

        self.organize_button = QPushButton("Organize Files")
        self.organize_button.clicked.connect(self.organize_files)
        self.layout.addWidget(self.organize_button)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        self.selected_files = []

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            self.selected_files = files
            self.file_list.clear()
            self.file_list.addItems(files)
            self.status_label.setText("Files selected successfully!")

    def organize_files(self):
        if not self.selected_files:
            self.status_label.setText("No files selected!")
            return

        sort_criteria = self.sort_criteria.currentText()
        folder_count = self.folder_count.value()
        target_dir = "organized_files"

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        if sort_criteria == "Date":
            self.organize_by_date(target_dir)
        elif sort_criteria == "Size":
            self.organize_by_size(target_dir, folder_count)
        elif sort_criteria == "Custom Category":
            self.organize_by_category(target_dir, folder_count)

        self.status_label.setText(f"Files organized in '{target_dir}'.")

    def organize_by_date(self, target_dir):
        for file_path in self.selected_files:
            if not os.path.isfile(file_path):
                continue

            # Get file creation time
            creation_time = QDateTime.fromSecsSinceEpoch(int(os.path.getmtime(file_path))).toString("yyyy-MM-dd")
            date_dir = os.path.join(target_dir, creation_time)

            if not os.path.exists(date_dir):
                os.makedirs(date_dir)

            shutil.copy(file_path, date_dir)

    def organize_by_size(self, target_dir, folder_count):
        # Group files by size (approx. evenly distribute)
        files_by_size = sorted(self.selected_files, key=lambda f: os.path.getsize(f))
        folders = [[] for _ in range(folder_count)]

        for i, file_path in enumerate(files_by_size):
            folders[i % folder_count].append(file_path)

        for i, folder_files in enumerate(folders):
            size_dir = os.path.join(target_dir, f"Folder_{i+1}")
            if not os.path.exists(size_dir):
                os.makedirs(size_dir)

            for file_path in folder_files:
                shutil.copy(file_path, size_dir)

    def organize_by_category(self, target_dir, folder_count):
        # Prompt user to define custom categories (for now, a basic categorization by extensions)
        categories = {}
        for file_path in self.selected_files:
            extension = os.path.splitext(file_path)[-1].lower()
            if extension not in categories:
                categories[extension] = []
            categories[extension].append(file_path)

        for i, (category, files) in enumerate(categories.items()):
            category_dir = os.path.join(target_dir, f"Category_{category[1:].upper()}")
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)

            for file_path in files:
                shutil.copy(file_path, category_dir)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec_())
