from StreamProcessing.Point import Point


class Direction:
    def __init__(self,first=Point(0,0),last=Point(0,0)):
        self.start_point = first
        self.end_point = last
