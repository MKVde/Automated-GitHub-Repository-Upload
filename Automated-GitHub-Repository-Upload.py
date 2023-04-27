from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon
import os
import sys
import subprocess
import requests
import json

class GitHubUploader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400) # x, y, width, height
        self.init_ui()
        app_icon = QIcon("C:\\Users\\abdir\\OneDrive\\Desktop\\Web Dev\\Web Scraping Learn\\Automated GitHub repository\\Upload Files to GitHub GUI\\github.ico")
        self.setWindowIcon(app_icon)

    def init_ui(self):
        self.github_repository_name_label = QtWidgets.QLabel("GitHub Repository Name:")
        self.github_repository_name_entry = QtWidgets.QLineEdit()

        self.github_username_label = QtWidgets.QLabel("GitHub Username:")
        self.github_username_entry = QtWidgets.QLineEdit()

        self.token_label = QtWidgets.QLabel("Token:")
        self.token_entry = QtWidgets.QLineEdit()
        self.token_entry.setEchoMode(QtWidgets.QLineEdit.Password)

        self.select_folder_button = QtWidgets.QPushButton("Select Folder")
        self.select_folder_button.clicked.connect(self.select_folder)

        self.upload_button = QtWidgets.QPushButton("Upload")
        self.upload_button.clicked.connect(self.upload_to_github)

        self.selected_folder_label = QtWidgets.QLabel("Selected Folder: ")
        self.selected_folder_entry = QtWidgets.QLineEdit()

        self.progress_bar = QtWidgets.QProgressBar()

        self.repository_status_label = QtWidgets.QLabel("")

        self.exit_button = QtWidgets.QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.github_repository_name_label)
        layout.addWidget(self.github_repository_name_entry)
        layout.addWidget(self.github_username_label)
        layout.addWidget(self.github_username_entry)
        layout.addWidget(self.token_label)
        layout.addWidget(self.token_entry)
        layout.addWidget(self.selected_folder_label)
        layout.addWidget(self.select_folder_button)
        layout.addWidget(self.selected_folder_entry)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.repository_status_label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)
        self.setWindowTitle("GitHub Uploader")

    def select_folder(self):
        selected_folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if selected_folder:
            self.selected_folder_entry.setText(selected_folder)

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def upload_to_github(self):
        # Get the inputs from the user
        github_repository_name = self.github_repository_name_entry.text()
        github_username = self.github_username_entry.text()
        token = self.token_entry.text()

        # Specify the path to the files to upload
        files_path = self.selected_folder_entry.text()

        # Change to the project directory
        os.chdir(files_path)

        # Check if the directory is a Git repository
        if subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True).stdout.decode().strip() != "true":
            # If not, initialize a new Git repository
            subprocess.run(["git", "init"])

        # Add all files to the git repository
        subprocess.run(["git", "add", "."])

        self.update_progress_bar(33)

        # Commit the changes
        subprocess.run(["git", "commit", "-m", "Initial commit"])

        self.update_progress_bar(66)

        # Check if the repository already exists
        response = requests.get(
            f"https://api.github.com/users/{github_username}/repos",
            headers={"Authorization": f"token {token}"},
        )

        if response.ok:
            repositories = json.loads(response.text)
            repository_exists = False

            for repository in repositories:
                if repository["name"] == github_repository_name:
                    repository_exists = True
                    break

            if repository_exists:
                # If the repository already exists, ask for confirmation before updating it
                confirm = QtWidgets.QMessageBox.question(
                    self,
                    "Confirmation",
                    "This repository already exists. Do you want to update it?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.No
                )
                if confirm == QtWidgets.QMessageBox.Yes:
                    subprocess.run(["git", "remote", "set-url", "origin", f"git@github.com:{github_username}/{github_repository_name}.git"])
                    subprocess.run(["git", "push", "-u", "origin", "master"])
            else:
                # If the repository does not exist, ask for confirmation before creating it
                confirm = QtWidgets.QMessageBox.question(
                    self,
                    "Confirmation",
                    "This repository does not exist. Do you want to create it?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.No
                )
                if confirm == QtWidgets.QMessageBox.Yes:
                    payload = {"name": github_repository_name}
                    response = requests.post(
                        "https://api.github.com/user/repos",
                        headers={"Authorization": f"token {token}"},
                        json=payload,
                    )

                    if response.ok:
                        QtWidgets.QMessageBox.information(self, "Information", "New repository created.")
                        subprocess.run(["git", "remote", "add", "origin", f"git@github.com:{github_username}/{github_repository_name}.git"])
                        subprocess.run(["git", "push", "-u", "origin", "master"])
                    else:
                        error_msg = f"Failed to create repository: {response.reason}"
                        QtWidgets.QMessageBox.warning(self, "Error", error_msg)

        else:
            error_msg = f"Failed to retrieve repositories: {response.reason}"
            QtWidgets.QMessageBox.warning(self, "Error", error_msg)
            self.update_progress_bar(0)
            QtWidgets.QMessageBox.critical(self, "Error", error_msg)

        self.update_progress_bar(100)
        QtWidgets.QMessageBox.information(self, "Information", "Process finished.")
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    uploader = GitHubUploader()
    uploader.show()
    sys.exit(app.exec_())
