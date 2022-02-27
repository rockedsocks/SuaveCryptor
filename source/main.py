from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QFile, QTextStream, Qt
from platform import system
from sys import argv
import dark_theme
import work
import filing


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # call inherited init method
        uic.loadUi('../resources/main.ui', self)
        self.setWindowTitle("SuaveCryptor Beta")
        self.setWindowIcon(QtGui.QIcon('../resources/wawa-comfort.ico'))
        self.e_custom_file_loc = self.findChild(QtWidgets.QCheckBox, 'custom_file_loc')
        self.d_custom_file_loc = self.findChild(QtWidgets.QCheckBox, 'custom_file_loc_2') # Checkboxes for custom output Paths
        self.use_key = self.findChild(QtWidgets.QCheckBox, 'use_key') # Checkbox for using existing key
        self.choose_key = self.findChild(QtWidgets.QPushButton, 'choose_key') # Button for selecting key
        self.key_loc = self.findChild(QtWidgets.QLabel, 'key_loc') # Label containing custom key path
        self.e_choose_save = self.findChild(QtWidgets.QPushButton, 'choose_save')
        self.e_save_loc = self.findChild(QtWidgets.QLabel, 'save_loc')
        self.d_choose_save = self.findChild(QtWidgets.QPushButton, 'choose_save_2')
        self.d_save_loc = self.findChild(QtWidgets.QLabel, 'save_loc_2') # Custom File Output stuff
        self.dk_choose = self.findChild(QtWidgets.QPushButton, 'dk_choose')
        self.ek_choose = self.findChild(QtWidgets.QPushButton, 'ek_choose') # Buttons for Selecting Keys
        self.ef_choose = self.findChild(QtWidgets.QPushButton, 'ef_choose')
        self.df_choose = self.findChild(QtWidgets.QPushButton, 'df_choose') # Buttons for Selecting Files
        self.d_file = self.findChild(QtWidgets.QPushButton, 'd_file')
        self.e_file = self.findChild(QtWidgets.QPushButton, 'e_file') # Buttons for starting Decryption/Encryption
        self.ek_location = self.findChild(QtWidgets.QLabel, 'ek_location')
        self.dk_location = self.findChild(QtWidgets.QLabel, 'dk_location') # Labels for Key Paths
        self.df_filename = self.findChild(QtWidgets.QLabel, 'df_filename')
        self.ef_filename = self.findChild(QtWidgets.QLabel, 'ef_filename') # Labels for Files
        self.dk_choose.clicked.connect(lambda: self.key_buttons(lambda: set_path(self.dk_location, self.choose_file("open", "Keys (*.key)"), [self.d_file], self.df_filename.text() != ""), self.d_text))
        self.ek_choose.clicked.connect(lambda: self.key_buttons(lambda: set_path(self.ek_location, self.choose_file("save", "Keys (*.key)"), [self.e_file], self.ef_filename.text() != ""), self.e_text))
        self.df_choose.clicked.connect(lambda: set_path(self.df_filename, self.choose_file("open", "Decrypted Files (*.pwn)"), [self.d_file], self.dk_location.text() != ""))
        self.ef_choose.clicked.connect(lambda: set_path(self.ef_filename, self.choose_file("open", "Any File (*)"), [self.e_file], self.ek_location.text() != "" or (self.use_key.isChecked() and self.key_loc.path != "")))
        self.e_file.clicked.connect(lambda: self.encrypt(True))
        self.d_file.clicked.connect(lambda: self.decrypt(True))
        self.use_key.toggled.connect(lambda: toggle_buttons([self.ek_choose, self.choose_key]))
        self.use_key.toggled.connect(lambda: self.e_text.setEnabled(self.use_key.isChecked()))
        self.d_custom_file_loc.toggled.connect(lambda: self.d_choose_save.setEnabled(not(self.d_choose_save.isEnabled())))
        self.e_custom_file_loc.toggled.connect(lambda: self.e_choose_save.setEnabled(not(self.e_choose_save.isEnabled()))) # Checkbox stuff
        self.e_choose_save.clicked.connect(lambda: set_path(self.e_save_loc, self.choose_file("save", "Encrypted Files (*.pwn)"), [self.e_file], (self.ek_location.text() != "" or (self.use_key.isChecked() and self.key_loc.text() != "")) and self.ef_filename.text() != ""))
        self.d_choose_save.clicked.connect(lambda: set_path(self.d_save_loc, self.choose_file("save", "Dencrypted Files (*)"), [self.d_file], self.dk_location.text() != "" and self.df_filename.text() != ""))
        self.choose_key.clicked.connect(lambda: self.key_buttons(lambda: set_path(self.key_loc, self.choose_file("open", "Key Files (*.key)"), [self.e_file], self.ef_filename.text() != ""), self.e_text))
        self.e_text.clicked.connect(lambda: self.encrypt(False))
        self.d_text.clicked.connect(lambda: self.decrypt(False))
        self.show()

    def choose_file(self, mode, types):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(dialog.ExistingFile)
        if mode == "open":
            dialog.setAcceptMode(dialog.AcceptOpen)
            return dialog.getOpenFileName(self, "Open File", "~/", types)
        else:
            dialog.setAcceptMode(dialog.AcceptSave)
            return dialog.getSaveFileName(self, "Save File", "~/", types)
            dialog.setFileMode
            return dialog.get

    def keyPressEvent(self, e): # escape app on pressing of Esc key
        if e.key() == Qt.Key_Escape:
            self.close()

    def encrypt(self, save):
        if save: # encrypting file
            if self.e_save_loc.text() != "" and self.e_custom_file_loc.isChecked(): # if theres a save location
                save_path = self.e_save_loc.path + ".pwn"
            else:
                save_path = self.ef_filename.path[:self.ef_filename.path.rfind(".")] + ".pwn"
            if self.use_key.isChecked() and self.key_loc.path != "":
                _, contents = work.encrypt(self.ef_filename.path, key=filing.read(self.key_loc.path), file=True)
            else:
                key, contents = work.encrypt(self.ef_filename.path, file=True)
                filing.save(self.ek_location.path + ".key", key)
            contents = contents.decode("utf-8")
            contents += self.ef_filename.path[self.ef_filename.path.rfind("."):]
            filing.save(save_path, contents)
            popup = QtWidgets.QMessageBox()
            popup.setIcon(popup.Information)
            popup.setText("Encryption Completed!")
            popup.setWindowTitle("Task Completed")
            popup.setDetailedText("Encrypted File saved to " + save_path)
            if not(self.use_key.isChecked()):
                popup.setDetailedText("Encrypted Files saved to " + save_path + "\nKey saved to " + self.ek_location.path + ".key")
            popup.setStandardButtons(popup.Ok)
            popup.exec_()

        else: # encrypting from text box
            if self.e_text_input.toPlainText() == "": # Warning for when there is no input
                popup = QtWidgets.QMessageBox()
                popup.setIcon(popup.Warning)
                popup.setText("Not All Fields Filled!")
                popup.setDetailedText("Text to encrypt not inputed!")
                popup.setStandardButtons(popup.Ok)
                popup.exec_()
            else:
                if self.key_loc.text() != "" and self.use_key.isChecked():
                    self.e_output.setText(work.encrypt(self.e_text_input.toPlainText(), key=filing.read(self.key_loc.path))[1])
                else:
                    key, result = work.encrypt(self.e_text_input.toPlainText())
                    self.e_output.setText(result)
                    filing.save(self.ek_location.path + ".key", key)

    def decrypt(self, save):
        if save: # decrypt file if save is true
            suffix = filing.read(self.df_filename.path)[filing.read(self.df_filename.path).rfind("."):]
            save_path = self.df_filename.path[:-4] + suffix
            filing.save(self.df_filename.path, filing.read(self.df_filename.path)[:0 - len(suffix)])
            if self.d_custom_file_loc.isChecked() and self.d_save_loc.path != "":
                save_path = self.d_save_loc.path + filing.read(self.df_filename.path)[filing.read(self.df_filename.path).rfind("."):]
            if self.d_custom_file_loc.isChecked() and self.d_save_loc.path != "":
                filing.save(self.d_save_loc.path + save_path[save_path.rfind("."):], work.decrypt(filing.read(self.df_filename.path), filing.read(self.dk_location.path), file=True))
            else:
                filing.save(save_path, work.decrypt(filing.read(self.df_filename.path), filing.read(self.dk_location.path), file=True))
            filing.save(self.df_filename.path, filing.read(self.df_filename.path) + suffix)
            popup = QtWidgets.QMessageBox() # popup to notify task completion
            popup.setIcon(popup.Information)
            popup.setText("Decryption Completed!")
            popup.setWindowTitle("Task Completed")
            popup.setDetailedText("Decrypted File saved to " + save_path)
            popup.setStandardButtons(popup.Ok)
            popup.exec_()
        else:
            inputs = self.findChild(QtWidgets.QTextBrowser, 'dt_input')
            if inputs.toPlainText() == "":
                popup = QtWidgets.QMessageBox()
                popup.setIcon(popup.Warning)
                popup.setText("Fill in the input!")
                pupup.setWindowTitle("Not all fields filled!")
                popup.setStandardButtons(popup.Ok)
                popup.exec_()
            else:
                print(filing.read(self.dk_location.path))
                self.findChild(QtWidgets.QTextBrowser, 'dt_output').setText(work.decrypt(inputs.toPlainText(), filing.read(self.dk_location.path)))

    def key_buttons(self, func, button):
        func()
        button.setEnabled(True)



def toggle_buttons(buttons):
    for button in buttons:
        button.setEnabled(not(button.isEnabled()))

def set_folder(label, path, ungray, req):
    label.path = path[0]
    if system() == "Windows":
        name = "\\" + path[0].split("\\")[-1]
    else:
        name = "/" + path[0].split("/")[-1]
    label.setText(name)
    label.path = path[0]
    if req and path[0] != "":
        for button in ungray:
            button.setEnabled(True)



def set_path(label, path, ungray, req): # ungray is button to ungray, but only if reqs (QPushButton) are filled
    if system() == "Windows":
        name = path[0].split("\\")
    else:
        name = path[0].split("/")
    name = name[len(name) - 1]
    label.path = path[0]
    label.setText(name)
    if req and path[0] != "":
        for button in ungray:
            button.setEnabled(True)

def main():
    app = QtWidgets.QApplication(argv)

    # set stylesheet
    # file = QFile("../resources/dark/stylesheet.qss")
    # file.open(QFile.ReadOnly | QFile.Text)
    # stream = QTextStream(file)
    # app.setStyleSheet(stream.readAll())
    # other stuff now
    window = Ui()
    app.exec_()


main()
