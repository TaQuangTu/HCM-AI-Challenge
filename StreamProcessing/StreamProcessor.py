import random

from StreamProcessing.Helpers import MathHelper
from StreamProcessing.Movement import Movement
from StreamProcessing.Point import Point


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
            intersect = MathHelper.is_on_polygon(obj, polygon=self.polygon)
            if intersect is not None:
                similar_objects_in_pre_frames = self.get_similar_objects(obj)
                if self.has_moved_out_already(similar_objects_in_pre_frames):
                    obj.moved_out = True
                    continue
                x1, y1, x2, y2 = intersect
                direction = self.__get_direction(x1, y1, x2, y2, obj)
                if direction is not None:
                    obj.moved_out = True
                    movement = Movement(direction, obj)
                    movements.append(movement)
        return movements

    def get_similar_objects(self, obje):
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
                    if not most_similar is None:
                        similar_objects.append(most_similar)
                        obje = most_similar

        return similar_objects

    def __get_most_similar(self, obje, list_of_object):
        weights = [0.25, 0.75]
        obje_diagonal_line = obje.calculate_diagonal_line()
        for obj in list_of_object:
            diagonal_line = obj.calculate_diagonal_line()
            obj.similar_score = weights[0] * 1 / abs(diagonal_line - obje_diagonal_line + 0.001) + weights[
                1] * obj.similar_score
        list_of_object.sort(key=lambda x: x.similar_score)
        highest_score = -1000000
        chosen_obj = None
        for obj in list_of_object:
            if obj.similar_score > highest_score:
                chosen_obj = obj
                highest_score = obj.similar_score
        return chosen_obj

    def __get_direction(self, x1, y1, x2, y2, obj):
        closest = 99999999
        chosen_direction = None
        for intersect in self.polygon.intersections:
            if intersect.vertice1.x != x1 or intersect.vertice1.y != y1 or intersect.vertice2.x != x2 or intersect.vertice2.y != y2:
                continue
            distance = MathHelper.distanceP2P(intersect.point, Point(obj.x_center, obj.y_center))
            if distance < closest:
                closest = distance
                chosen_direction = intersect.direction
        if chosen_direction is not None:
            if MathHelper.distanceP2P(Point(obj.x_center, obj.y_center),
                                      chosen_direction.start_point) < MathHelper.distanceP2P(
                Point(obj.x_center, obj.y_center), chosen_direction.end_point):
                chosen_direction = None
        return chosen_direction

    def has_moved_out_already(self, similars):
        if len(similars) > 0 and similars[0].moved_out == True:
            return True
        return False
