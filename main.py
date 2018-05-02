# -*- encoding: utf-8 -*-
from Ui.MainUi import Main_Ui
import sys
from PyQt5 import QtWidgets

class Main(Main_Ui):
    def __init__(self):
        Main_Ui.__init__(self)
        self.start_button.clicked.connect(self.clicked)
    def clicked(self):
        self.door_state_label.setText('10')
        print("test button clicked function")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
