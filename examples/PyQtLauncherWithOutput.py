#!/usr/bin/env python3
#This example shows a simple launcher with PyQt that shows the output of Minecraft in a text filed
from PyQt6.QtWidgets import QApplication, QWidget, QPlainTextEdit, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import QProcess
import minecraft_launcher_lib
import sys

class GameOutputWidget(QPlainTextEdit):
    def __init__(self,launch_button):
        super().__init__()
        self.setReadOnly(True)
        self.launch_button = launch_button
        #Disable line wrap
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

    def display_output(self):
        #This function displays the output of Minecraft in the text field
        cursor = self.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(bytes(self.process.readAll()).decode())
        cursor.movePosition(cursor.MoveOperation.End)
        self.ensureCursorVisible()

    def execute_command(self,command):
        #QProcess.start takes as first argument the program and as second the list of arguments
        #So we need the filter the program from the command
        arguments = command[1:]
        #Deactivate the launch button
        self.launch_button.setEnabled(False)
        #Clear the text  field
        self.setPlainText("")
        self.process = QProcess(self)
        #Activate the launch button when Minecraft is closed
        self.process.finished.connect(lambda: self.launch_button.setEnabled(True))
        #Connect the function to display the output
        self.process.readyRead.connect(self.dataReady)
        #Start Minecraft
        self.process.start("java",arguments)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.version_select = QComboBox()
        launch_button = QPushButton("Launch")
        self.output_widget = GameOutputWidget(launch_button)

        #Set the password field to display *
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        launch_button.clicked.connect(self.launch_minecraft)

        #Add all versions to the Version ComboBox
        self.minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        for i in minecraft_launcher_lib.utils.get_available_versions(self.minecraft_directory):
            #Only add release versions
            if i["type"] == "release":
                self.version_select.addItem(i["id"])

        #Create the layouts
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(QLabel("Username:"))
        bottom_layout.addWidget(self.username_edit)
        bottom_layout.addWidget( QLabel("Password:"))
        bottom_layout.addWidget(self.password_edit)
        bottom_layout.addWidget(QLabel("Version:"))
        bottom_layout.addWidget(self.version_select)
        bottom_layout.addWidget(launch_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.output_widget)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle("PyQt Launcher with Output")

    def launch_minecraft(self):
        #Get the selected version
        version = self.version_select.currentText()

        #Make sure the version is installed
        minecraft_launcher_lib.install.install_minecraft_version(version,self.minecraft_directory)

        #Login
        login_data = minecraft_launcher_lib.account.login_user(self.username_edit.text(),self.password_edit.text())

        #Check if the login is correct
        if "errorMessage" in login_data:
            message_box = QMessageBox()
            message_box.setWindowTitle("Invalid credentials")
            message_box.setText("Invalid username or password")
            message_box.setStandardButtons(QMessageBox.StandardButtons.Ok)
            message_box.exec()
            return

        options = {
            "username": login_data["selectedProfile"]["name"],
            "uuid": login_data["selectedProfile"]["id"],
            "token": login_data["accessToken"]
        }

        #Get the command
        command = minecraft_launcher_lib.command.get_minecraft_command(version,self.minecraft_directory,options)

        #Call the function from the 
        self.output_widget.execute_command(command)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
