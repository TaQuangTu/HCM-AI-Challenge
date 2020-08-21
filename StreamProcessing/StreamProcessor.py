import random

from StreamProcessing.Helpers import MathHelper
from StreamProcessing.Movement import Movement
from StreamProcessing.Point import Point


class StreamProcessor:
    number_of_frames = 30  # correspond to 3s

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
            similar_objects_in_pre_frames = self.get_similar_objects(obj)
            if MathHelper.is_on_polygon(obj, polygon=self.polygon) and MathHelper.is_in_polygon(obj,self.polygon):
                if self.__has_on_polygon_before(similar_objects_in_pre_frames):
                    obj.moved_out = True
                    continue
                if self.__obj_is_moving_out(obj, similar_objects_in_pre_frames):
                    obj.moved_out = True
                    direction = self.__get_direction(similar_objects_in_pre_frames)
                    movement = Movement(direction, obj)
                    movements.append(movement)
        return movements

    def get_similar_objects(self, obje):
        num_of_similar_for_each_frame = 3
        similar_objects = []
        if len(self.frames) > 1:
            for frame in self.frames[1:]:
                if len(frame.objects) > 0:
                    for obj in frame.objects:
                        similar_score = obje.get_similar_score(obj)
                        obj.similar_score = similar_score
                    frame.objects.sort(key=lambda x: x.similar_score)
                    # pick up 3 objects that are most similar to obje
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
        highest_score = -1
        chosen_obj = None
        for obj in list_of_object:
            distance = MathHelper.distanceP2P(Point(obje.x_center, obje.y_center), Point(obj.x_center, obj.y_center))
            if obj.similar_score > highest_score and obj.class_type == obje.class_type and float(
                    obj.confident_score) > 0.3 and distance < obje_diagonal_line:
                chosen_obj = obj
                highest_score = obj.similar_score
        return chosen_obj

    def __get_direction(self, similar_objects_in_pre_frames):
        min_score = 7500000
        chosen = None
        for direction in self.polygon.moving_directions:
            p1 = direction.start_point
            p2 = direction.end_point
            score = 0
            for obj in similar_objects_in_pre_frames:
                p3 = Point(obj.x_center, obj.y_center)
                score = score + MathHelper.distanceP2Line(p1, p2, p3)
            if score < min_score:
                chosen = direction
                min_score = score

        return chosen

    def __obj_is_moving_out(self, obj, similars):
        outs = 0
        ins = 0
        is_in = MathHelper.is_in_polygon(obj, polygon=self.polygon)
        if is_in:
            ins += 1
        else:
            outs += 1
        for similar in similars:
            is_in = MathHelper.is_in_polygon(similar, polygon=self.polygon)
            if is_in:
                ins += 1
            else:
                outs += 1
        return ins > outs

    def __has_on_polygon_before(self, similars):
        if len(similars) > 0 and similars[0].moved_out == True:
            return True
        return False
