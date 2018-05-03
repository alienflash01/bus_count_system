# -*- encoding: utf-8 -*-
from Ui.MainUi import Main_Ui
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from src import utils
import time
from tmp import Tmp_Thread

class Main(Main_Ui):
    def __init__(self):
        Main_Ui.__init__(self)
        
        self.start_button.clicked.connect(self.start_works)
        self.pause_button.clicked.connect(self.stop_works)

        self.init_works()

    def init_works(self):
        self.tmp_thread = Tmp_Thread()
        self.tmp_thread.video_signal.connect(self.show_video)

        self.tmp_thread.result_signal.connect(self.show_result)
    
    def start_works(self):
        self.tmp_thread.start()
    
    def show_video(self,videoframe):
        self.videoframe=videoframe.scaled(self.video_label.size())
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(self.videoframe))  

    def stop_works(self):
        self.tmp_thread.stop_video()
    
    def show_result(self, result):
        self.door_state_label.setText(result['door_state'])
        self.crowd_counted_label.setText(result['crowd_nums'])
        self.crossline_counted_label.setText(result['cross_num'])
        self.crossline_sum_counted_label.setText(result['cross_all_num'])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())