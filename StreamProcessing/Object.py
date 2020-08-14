from math import sqrt

from StreamProcessing.Direction import Direction
from StreamProcessing.Helpers import MathHelper
from StreamProcessing.Point import Point


class Object:
    AREA_BIAS_THRESHOLD = 0.25
    DISTANCE_SIMILAR_THRESHOLD = 20 # unit:px
    CONFIDENT_THRESHOLD = 0.85
    type1 = ["bicycle", "motorbike"]
    type2 = ["car"]
    type3 = ["bus"]
    type4 = ["train", "truck"]
    ObjectType = {
        0: ("None"),
        1: ("bicycle", "motorbike"),
        2: ("car"),
        3: ("bus"),
        4: ("train", "truck")
    }

    def __init__(self, class_name = "None", confident_score=0, x_center=-1,y_center=-1,width=-1,height=-1):
        self.confident_score = confident_score
        self.class_name = class_name
        self.set_class_name(class_name)
        self.x_center = x_center
        self.y_center = y_center
        self.width = width
        self.height = height
        self.moving_direction = Direction()

    def set_class_name(self, class_name):
        self.class_name = class_name
        for key in Object.ObjectType:
            if class_name in Object.ObjectType[key]:
                self.class_type = key
                return
                # else
        self.class_type = 0

    # Check if an object is valid
    def is_valid(self):
        if self.class_type == 0:
            return False
        if self.x_center < 0:
            return False
        if self.y_center < 0:
            return False
        if self.width < 0:
            return False
        if self.height < 0:
            return False
        return True

    # compare if two objects is one
    def get_similar_score(self, other_object):
        distance = MathHelper.distanceP2P(Point(self.x_center,self.y_center),Point(other_object.x_center,other_object.y_center))
        return 1/(distance+0.001)

    def calculate_diagonal_line(self):
        return sqrt(self.width**2+self.height**2)