# -*- encoding:utf-8 -*-
# the main ui setting

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys
class Main_Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setGeometry(20,20,1280,720)
        self.setWindowTitle('公家车人群计数系统')
        
        #设置上方布局
        main_above_hbox = QHBoxLayout() #主界面上方布局
        self.video_label = self.set_label('')
        #self.video_label.resize(960, 540)
        self.video_label.setFixedSize(960,540)
        
        above_right_bbox = self.set_above_right_layout()
        main_above_hbox.addWidget(self.video_label)
        main_above_hbox.addLayout(above_right_bbox)

        main_above_hbox.setStretch(0,3)
        main_above_hbox.setStretch(1,1)

        #设置下方布局
        main_blew_hbox = self.set_blew_layout()

        #总的布局
        main_vbox = QVBoxLayout()
        main_vbox.addLayout(main_above_hbox)
        main_vbox.addLayout(main_blew_hbox)
        main_vbox.setStretch(0,3)
        main_vbox.setStretch(1,1)

        self.setLayout(main_vbox)

    def set_above_right_layout(self):
        ## 设置核心布局
        child_right_Gridbox = QGridLayout()
        child_right_Gridbox.setSizeConstraint(QLayout.SetMinAndMaxSize)
        child_right_Gridbox.setColumnStretch(1, 4)
        child_right_Gridbox.setColumnStretch(2, 4)
        
        self.door_state_label = self.set_label('关门','l')
        self.crowd_counted_label = self.set_label('0','l')
        self.crossline_counted_label = self.set_label('0','l')
        self.crossline_sum_counted_label = self.set_label('0','l')
        
        self.show_door_state_label = self.set_label('车门状态','l')
        self.show_crowd_counted_label = self.set_label('车内人数','l')
        self.show_crossline_counted_label = self.set_label('下车总人数','l')
        self.show_crossline_sum_counted_label = self.set_label('当前下车人数','l')
        
        #设置布局内容
        child_right_Gridbox.addWidget(self.show_door_state_label,0,0)
        child_right_Gridbox.addWidget(self.door_state_label,0,1)
        child_right_Gridbox.addWidget( self.show_crowd_counted_label ,1,0)
        child_right_Gridbox.addWidget(self.crowd_counted_label,1,1)
        child_right_Gridbox.addWidget(self.show_crossline_counted_label,2,0)
        child_right_Gridbox.addWidget(self.crossline_counted_label,2,1)
        child_right_Gridbox.addWidget(self.show_crossline_sum_counted_label,3,0)
        child_right_Gridbox.addWidget(self.crossline_sum_counted_label,3,1)
        
        #设置布局比例
        child_right_Gridbox.setColumnStretch(0,5)
        child_right_Gridbox.setColumnStretch(1,1)
        for i in range(4):
            child_right_Gridbox.setRowStretch(i,4)

        # 设置总的布局
        above_right_layout = QVBoxLayout()
        above_right_layout.addStretch(1)
        above_right_layout.addLayout(child_right_Gridbox)
        above_right_layout.addStretch(4)

        return above_right_layout

    def set_blew_layout(self):
        self.start_button = QPushButton('start')
        self.pause_button = QPushButton('pause')
        self.select_button = QPushButton('select_file')
        main_blew_hbox = QHBoxLayout() #主界面下方布局
        main_blew_hbox.addStretch(1)
        main_blew_hbox.addWidget(self.start_button)
        main_blew_hbox.addStretch(1)
        main_blew_hbox.addWidget(self.pause_button)
        main_blew_hbox.addStretch(1)
        main_blew_hbox.addWidget(self.select_button)
        main_blew_hbox.addStretch(1)  
        return main_blew_hbox

    def set_label(self, label_name, aligndirction = None):
        label = QLabel(label_name)
        label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        if aligndirction == 'r':
            label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        elif aligndirction == 'l':
            label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        else:
            pass
        return label
