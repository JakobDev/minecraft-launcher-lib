#!/usr/bin/env python3
# This example shows how to install Minecraft with a ProgressBar in PyQt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QProgressBar, QFileDialog, QFormLayout, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal
import minecraft_launcher_lib
import sys


class InstallThread(QThread):
    progress_max = pyqtSignal("int")
    progress = pyqtSignal("int")
    text = pyqtSignal("QString")

    def __init__(self) -> None:
        QThread.__init__(self)
        self._callback_dict = {
            "setStatus": lambda text: self.text.emit(text),
            "setMax": lambda max_progress: self.progress_max.emit(max_progress),
            "setProgress": lambda progress: self.progress.emit(progress),
        }

    def set_data(self, version: str, directory) -> None:
        self._version = version
        self._directory = directory

    def run(self) -> None:
        minecraft_launcher_lib.install.install_minecraft_version(self._version, self._directory, callback=self._callback_dict)


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._install_thread = InstallThread()

        self._version_combo_box = QComboBox()
        self._path_edit = QLineEdit()
        self._path_browse_button = QPushButton("Browse")
        self._progress_bar = QProgressBar()
        self._install_single_thread_button = QPushButton("Install Single Thread")
        self._install_multi_thread_button = QPushButton("Install Multi Thread")

        for i in minecraft_launcher_lib.utils.get_version_list():
            self._version_combo_box.addItem(i["id"])

        self._path_edit.setText(minecraft_launcher_lib.utils.get_minecraft_directory())

        self._progress_bar.setTextVisible(True)

        self._install_thread.progress_max.connect(lambda maximum: self._progress_bar.setMaximum(maximum))
        self._install_thread.progress.connect(lambda value: self._progress_bar.setValue(value))
        self._install_thread.text.connect(lambda text: self._progress_bar.setFormat(text))
        self._install_thread.finished.connect(self._install_thread_finished)

        self._path_browse_button.clicked.connect(self._path_browse_button_clicked)
        self._install_single_thread_button.clicked.connect(self._install_minecraft_single_thread)
        self._install_multi_thread_button.clicked.connect(self._install_minecraft_multi_thread)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self._path_edit)
        path_layout.addWidget(self._path_browse_button)

        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Version:"), self._version_combo_box)
        form_layout.addRow(QLabel("Path:"), path_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self._install_single_thread_button)
        button_layout.addWidget(self._install_multi_thread_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self._progress_bar)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("PyQtInstallation")

    def _install_thread_finished(self) -> None:
        # This function is called after the Multi Thread Installation has been finished
        self._install_single_thread_button.setEnabled(True)
        self._install_multi_thread_button.setEnabled(True)

    def _path_browse_button_clicked(self) -> None:
        path = QFileDialog.getExistingDirectory(self, directory=self._path_edit.text())
        if path != "":
            self._path_edit.setText(path)

    def _install_minecraft_single_thread(self) -> None:
        # This function installs Minecraft in the same Thread as the GUI
        # This is much simpler than using a other Thread, but the GUI will freeze until the function is completed
        callback = {
            "setStatus": lambda text: self._progress_bar.setFormat(text),
            "setProgress": lambda value: self._progress_bar.setValue(value),
            "setMax": lambda maximum: self._progress_bar.setMaximum(maximum)
        }

        minecraft_launcher_lib.install.install_minecraft_version(self._version_combo_box.currentText(), self._path_edit.text(), callback=callback)

    def _install_minecraft_multi_thread(self) -> None:
        # This functions installs Minecraft on a other Thread than the GUI
        # This is more complex than using the same Thread, but the GUI will not freeze
        self._install_single_thread_button.setEnabled(False)
        self._install_multi_thread_button.setEnabled(False)

        self._install_thread.set_data(self._version_combo_box.currentText(), self._path_edit.text())
        self._install_thread.start()


def main():
    app = QApplication(sys.argv)

    w = Window()
    w.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
