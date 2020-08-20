from .Object import Object


class Frame:
    def __init__(self, video_name="0", frame_id=-1):
        self.video_name = video_name
        self.frame_id = frame_id
        self.objects = []  # storage list of objects

    def has_objects(self):
        return len(self.objects) != 0

    def remove_invalid_objects(self):
        for obj in self.objects:
            if not obj.is_valid():
                self.objects.remove(obj)

    def add_object(self, new_object):
        self.objects.append(new_object)
