#临时文件
from PyQt5 import QtCore, QtGui
import time, cv2
from src import utils
class Tmp_Thread(QtCore.QThread):
    video_signal = QtCore.pyqtSignal(QtGui.QImage)
    result_signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent = None):
        super(Tmp_Thread, self).__init__()
        self.stop = False
    def __del__(self):
        self.wait()

    def run(self):
        cv_video = cv2.VideoCapture('demo.avi')
        is_readed = True
        tmp_i = 0
        if cv_video.isOpened():
            is_readed, frame = cv_video.read()
        else:
            print('open video faild')
        while True:
            time.sleep(0.07) #延时，以播放
            is_readed, frame = cv_video.read()
            video_frame = utils.im_to_qimage(frame)

            result = self.detector(frame, tmp_i)
            self.result_signal.emit(result)
            tmp_i += 1
            # if result[state] == 'open':
            #     self.tracker(result)
            # else:
            #     self.count(result)

            self.video_signal.emit(video_frame)
            if self.stop == True:
                cv_video.release()
                break
    
    def stop_video(self):
        self.stop = True
    
    def detector(self,frame, tmp_i):
        n0 = 'ahah'
        if tmp_i%10 == 0:
            n0 = 'open'
        elif tmp_i%13 == 0:
            n0 = 'clos'
        else:
            no = 'unsu'
        n1 = str(tmp_i * 4 )
        n2 = str(tmp_i * 2 )
        n3 = str(tmp_i)
        result={'door_state':n0,
                'crowd_nums':n1,
                'cross_num':n2,
                'cross_all_num':n3}
        return result