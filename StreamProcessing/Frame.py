from .Object import Object


class Frame:
    def __init__(self):
        self.objects = []  # storage list of objects

    def has_objects(self):
        return len(self.objects) != 0

    def remove_invalid_objects(self):
        for obj in self.objects:
            if not obj.is_valid():
                self.objects.remove(obj)
