import random

from StreamProcessing.Direction import Direction
from StreamProcessing.Frame import Frame
from StreamProcessing.Helpers import MathHelper
from StreamProcessing.Movement import Movement
from StreamProcessing.Point import Point
from StreamProcessing.Polygon import Polygon


class StreamProcessor:
    number_of_frames = 20  # correspond to 2s

    def __init__(self, moving_directions, polygon):
        self.frames = []
        self.polygon = polygon
        self.polygon.moving_directions = moving_directions

    def __add_new_frame(self, new_frame):
        self.frames.insert(0, new_frame)
        if len(self.frames) > StreamProcessor.number_of_frames:
            self.frames.pop()

    # this function return list of movements
    def process_new_frame(self, new_frame):
        self.__add_new_frame(new_frame)
        movements = []
        for obj in new_frame.objects:
            if MathHelper.is_on_polygon(Point(obj.x_center, obj.y_center), polygon=self.polygon):
                similar_objects_in_pre_frames = self.__get_similar_objects(obj)
                direction = self.__get_direction(similar_objects_in_pre_frames)
                movement = Movement(direction, obj)
                movements.append(movements)
        return movements

    def __get_similar_objects(self, obje):
        similar_objects = []
        if len(self.frames) > 1:
            for frame in self.frames[1:]:
                for obj in frame.objects:
                    similar_score = obje.get_similar_score(obj)
                    if len(similar_objects) <= 0:
                        similar_objects.append(obj)
                        obj.similar_score = similar_score
                    else:
                        for similar in similar_objects:
                            if similar_score > similar.similar_score:
                                similar_objects.append(obj)
                                obj.similar_score = similar_score
                                if len(similar_objects) > 10:
                                    similar_objects.remove(similar)
                                break
        return similar_objects

    def __get_direction(self, similar_objects_in_pre_frames):
        i = random.randint(0, len(self.polygon.moving_directions) - 1)
        direction = self.polygon.moving_directions[i]
        return direction
