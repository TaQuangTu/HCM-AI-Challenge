class Object:
    type1 = ["bicycle", "motorbike"]
    type2 = ["car"]
    type3 = ["bus"]
    type4 = ["train", "truck"]
    ObjectType = {
        0: None,
        1: ("bicycle", "motorbike"),
        2: ("car"),
        3: ("bus"),
        4: ("train", "truck")
    }

    def __init__(self):
        self.class_type = Object.ObjectType[0]
        self.x_center = -1
        self.y_center = -1
        self.width = -1
        self.height = -1
        self.moving_direction

    #Check if an object is valid
    def is_valid(self):
        if self.class_name ==Object.ObjectType[0]:
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
