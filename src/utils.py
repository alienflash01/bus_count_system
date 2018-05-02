from PyQt5 import QtGui
# import numpy as np
# import cv2


def im_to_qimage_nochannel(img):
    rotated_im = img.copy()    
    height, width, channel = rotated_im.shape
    bytesPerLine = 3 * width
    qImg = QtGui.QImage(rotated_im.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
    return qImg

def im_to_qimage(img):
    img_matlab = img.copy()
    tmp = img_matlab[:,:,2].copy()
    img_matlab[:,:,2] = img_matlab[:,:,0]
    img_matlab[:,:,0] = tmp 
    img_rotated = img_matlab
    height, width, channel = img_rotated.shape
    bytesPerLine = 3 * width
    qImg = QtGui.QImage(img_rotated.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
    return qImg