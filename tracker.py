# -*- coding = utf-8 -*-
from src import utils
import os
import cv2
import numpy as np

# 最小iou和最大的两点间的距离
# 追踪
IOU_THRESHOLD = 0.005
DIS_THRESHOLD = 30

# 计数相关参数
"""
计数算法的一些关键约束：
"""
DIVIDER_THRESHOLD =  100 #划线检测的位置
Y_DISTANCE_THRESHOLD = 20 #行人在Y方向运动的距离阈值

line2 = 30 #上一条线的位置

MAX_UNSEEN_FRAMES = 2


class People(object):
    
    def __init__(self, id, position):
        self.id = id
        self.positions = [position] 
        self.counted = False
        self.unseen_frame = 0  # 没有被看到的帧数
        self.position_num = 0  # 含有的位置个数        
        self.lowest_position = position
        self.track_position_num = 0 # 通过追踪添加的位置个数

    @property
    def last_position(self):

        return self.positions[-1]

    @property
    def first_position(self):
        return self.positions[0]

    @property
    def max_y_distance(self):
    # y方向上最大的运动距离（最低点到消失点的距离）
        last_position = self.last_position[1]
        lowest_position = self.lowest_position[1]
        distance = abs(last_position[1] - lowest_position[1])        
        return distance

    def update_lowest_position(self, new_position):
        if self.lowest_position[1][1] < new_position[1][1]:
            self.lowest_position = new_position

    def is_up(self):
    # 在Y方向上的整体趋势是否为向上
        dy = self.last_position[1] -  self.lowest_position[1]
        if dy > 0:
            return False
        else:
            return True

    def is_cross_line(self, divider):
        return self.last_position[1][1] < divider

    def is_cross_zone(self, divider):
        #最后2个点过线
        for item in range(-2,0):
            if self.positions[item][1][1] > divider:
                return False
        if self.lowest_position[1][1] < divider:
            return False
        return True
        
    def add_position(self, new_position):
        self.update_lowest_position(new_position)
        self.positions.append(new_position)    
        self.unseen_frame = 0
        self.position_num += 1

# =======================================================

class Peoples(object):
    def __init__(self):
        self.peoples = []
        self.next_people_id = 0
        self.people_count = 0
        self.max_unseen_frames = MAX_UNSEEN_FRAMES # 7
        self.iou_threshold = IOU_THRESHOLD # 0.01
        self.dis_threshold = DIS_THRESHOLD # 20
        self.divider = DIVIDER_THRESHOLD # 75
        self.y_distance_threshold = Y_DISTANCE_THRESHOLD # 50
        self.min_position_num = 0 # 必须出现15个点，才认为这个人是有效的，消除一现而过的情况

        self.is_zz = False
    
    def update_people(self, people, detected_position_list):
        # 在detected_position_list 中寻找people的下一帧 position
        cur_bbox, cur_point = people.last_position
        max_iou = self.iou_threshold
        valid_position = None
        
        #在新一帧所有bbox中，选取IOU最大的一个
        for item, position in enumerate(detected_position_list):
            bbox, point = position
            iou_score = utils.compute_iou(cur_bbox, bbox)
            if iou_score > max_iou:
                max_iou = iou_score
                valid_position = position
                valid_item = item
        
        if valid_position == None:
            people.unseen_frame += 1
            return None
        
        else:
            valid_point = valid_position[1]
            point_dis_score = utils.compute_distance(cur_point, valid_point)
            
            if point_dis_score > self.dis_threshold:
                people.unseen_frame += 1
                return None
            else:
                people.add_position(valid_position)
                return valid_item
    
    def counted_people(self):
        """ 根据行人是否进入某个区域进行计数
        算法描述：
        对图像，画一个矩形框（画线）
        1. 判断矩形框内是否有人，如果有人的话，如果该人运动向上运动 N 个像素点并消失，则计数
        2. 不在矩形框的人，如果进入矩形框，并运动 M 个像素点，并消失，则计数
        3. 添加对行人的约束：如果从出现到消失，小于60个像素点，则认为是误检
        """
        for people in self.peoples:
            if people.unseen_frame >= self.max_unseen_frames and people.position_num > self.min_position_num:
                if not people.counted \
                and people.is_up \
                and people.is_cross_zone(self.divider) \
                and people.max_y_distance > self.y_distance_threshold \
                and people.last_position[1][0] > 70 \
                and people.last_position[1][0] < 290 \
                and not people.counted:
                    self.people_count += 1
                    people.counted = True 

    def update_peoples(self, detected_position_list):
        for people in self.peoples:
            item = self.update_people(people, detected_position_list)
            if item is not None:
                del detected_position_list[item]
        
        for position in detected_position_list:
            new_people = People(self.next_people_id, position)
            self.next_people_id += 1
            self.peoples.append(new_people)
        
        # 计数
        #self.counted_people_crossline()
        self.counted_people()

        # Remove vehicles that have not been seen long enough
        removed = [] #被移除的people
        for people in self.peoples:
            if people.unseen_frame >= self.max_unseen_frames:
                removed.append(people.id)
                if people.position_num < self.min_position_num: 
                    self.next_people_id = self.next_people_id - 1
        self.peoples[:] = [ v for v in self.peoples
            if not v.unseen_frame >= self.max_unseen_frames]