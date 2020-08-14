import random

from StreamProcessing.Direction import Direction
from StreamProcessing.Frame import Frame
from StreamProcessing.Helpers import MathHelper
from StreamProcessing.Movement import Movement
from StreamProcessing.Point import Point
from StreamProcessing.Polygon import Polygon


class StreamProcessor:
    number_of_frames = 20  # correspond to 2s

    def __init__(self, polygon):
        self.frames = []
        self.polygon = polygon

    def __add_new_frame(self, new_frame):
        self.frames.insert(0, new_frame)
        if len(self.frames) > StreamProcessor.number_of_frames:
            self.frames.pop()

    # this function return list of movements
    def process_new_frame(self, new_frame):
        self.__add_new_frame(new_frame)
        movements = []
        for obj in new_frame.objects:
            if MathHelper.is_on_polygon(obj, polygon=self.polygon):
                similar_objects_in_pre_frames = self.__get_similar_objects(obj)
                direction = self.__get_direction(similar_objects_in_pre_frames)
                movement = Movement(direction, obj)
                movements.append(movement)
        return movements

    def __get_similar_objects(self, obje):
        num_of_similar_for_each_frame = 4
        similar_objects = []
        if len(self.frames) > 1:
            for frame in self.frames[1:]:
                if len(frame.objects) > 0:
                    for obj in frame.objects:
                        similar_score = obje.get_similar_score(obj)
                        obj.similar_score = similar_score
                    frame.objects.sort(key=lambda x: x.similar_score)
                    # pick up 4 objects that are most similar to obje
                    if len(frame.objects) > num_of_similar_for_each_frame:
                        most_similar = self.__get_most_similar(obje, frame.objects[-num_of_similar_for_each_frame:])
                    else:
                        most_similar = self.__get_most_similar(obje, frame.objects)
                    similar_objects.append(most_similar)
                    obje = most_similar

        return similar_objects

    def __get_most_similar(self, obje, list_of_object):
        weights = [0.4, 0.6]
        obje_diagonal_line = obje.calculate_diagonal_line()
        for obj in list_of_object:
            diagonal_line = obj.calculate_diagonal_line()
            obj.similar_score = weights[0] * 1 / abs(diagonal_line - obje_diagonal_line) + weights[
                1] * obj.similar_score
        list_of_object.sort(key=lambda x: x.similar_score)
        highest_score = -1
        chosen_obj = None
        for obj in list_of_object:
            if obj.similar_score > highest_score:
                chosen_obj = obj
                highest_score = obj.similar_score
        return chosen_obj

    def __get_direction(self, similar_objects_in_pre_frames):
        # TODO
        i = random.randint(0, len(self.polygon.moving_directions) - 1)
        direction = self.polygon.moving_directions[i]
        return direction
