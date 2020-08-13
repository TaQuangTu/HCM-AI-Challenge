from StreamProcessing.Direction import Direction
from StreamProcessing.Frame import Frame
from StreamProcessing.Polygon import Polygon


class StreamProcessor:
    number_of_frames = 20  # correspond to 2s

    def __init__(self, moving_directions, vertices):
        self.frames = []
        self.polygon = Polygon()
        self.polygon.list_points = vertices
        self.polygon.moving_directions = moving_directions

    def __add_new_frame(self, new_frame):
        if not new_frame is Frame:
            raise Exception("Not a frame exception")
        self.frames.insert(0, new_frame)
        if len(self.frames) > StreamProcessor.number_of_frames:
            self.frames.pop()

    def process_new_frame(self, new_frame):
        self.__add_new_frame(new_frame)
        for obj in new_frame.objects:
            # TODO: looking back previous frames to calculate moving direction of this object
            obj.moving_direction = Direction()
        return obj
