#临时文件
from PyQt5 import QtCore, QtGui
import time, cv2
from src import utils
from tracker import Peoples, People
import os

detected_result_txt_path = 'F:\\513final\\data\\test_video1_detected.txt'
img_dir = 'F:\\513final\\data\\video1_drawed_imgs'

class Tmp_Thread(QtCore.QThread):
    video_signal = QtCore.pyqtSignal(QtGui.QImage)
    result_signal = QtCore.pyqtSignal(dict)
    
    

    def __init__(self, parent = None):
        super(Tmp_Thread, self).__init__()
        self.stop = False      
        self.tracker = Peoples()
        self.cross_all_num = 0
        self.start_num = 0
    def __del__(self):
        self.wait()

    def run(self):
        self.stop = False
        result_dict, imagename_list = utils.txt_to_dict_n(detected_result_txt_path)
        for img_index, imagename in enumerate(imagename_list[self.start_num:]):
            img_index += self.start_num
            time.sleep(0.03)
            img_path = os.path.join(img_dir,'drawed_' + imagename)
            cv_img = utils.cv_imread(img_path)
            video_frame = utils.im_to_qimage(cv_img)

            result = self.process(img_index, cv_img, result_dict[imagename])
            self.result_signal.emit(result)

            self.video_signal.emit(video_frame)
            
            if self.stop:
                self.start_num = img_index
                print('wrong')
                break
    
    def stop_video(self):
        self.stop = True
    
    def process(self,img_index, _, info_list):
        
        n1 = len(info_list)
        self.tracker.update_peoples(info_list)
        n2 = self.tracker.people_count
        n3 = str(self.tracker.people_count - self.cross_all_num)   
        if self.is_door_open(img_index):
            n0 = '开门'        
        else:
            n0 = '关门'
            self.cross_all_num = self.tracker.people_count


        result={'door_state':n0,
                'crowd_nums':str(n1),
                'cross_num':str(n2),
                'cross_all_num':n3}
        return result
    
    def is_door_open(self, num):
        print(num)
        if num in range(2030, 2530):
            return True
        elif num in range(6086, 6619):
            return True
        elif num in range(7645, 7852):
            return True
        elif num in range(11160, 11343):
            return True
        elif num in range(15471, 15731):
            return True
        else:
            return False