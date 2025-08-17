import math


class Component():
    TYPES = ["R", "C", "L"]
    COUNTERS = [0, 0, 0]

    def __init__(self, prefix, type, parameter):
        self.parameter = parameter
        self.type = type

        # Increment the components counter
        idx = Component.TYPES.index(type)
        if idx >= 0:
            self.name = type + str(Component.COUNTERS[idx])+"{"+prefix + "}"
            Component.COUNTERS[idx] += 1
        else:
            raise ValueError("Error:Unknown component type")

    def getValue(self, frequency):
        Re, Im = 0, 0
        if self.type == Component.TYPES[0]:
            Re = self.parameter
        elif self.type == Component.TYPES[1]:
            Im = (-1/(2*math.pi*self.parameter*frequency))
        else:
            Im = (2*math.pi*self.parameter*frequency)
        return Re, Im

    @staticmethod
    def get_typeResistor():
        return Component.TYPES[0]

    @staticmethod
    def get_typeCapacitor():
        return Component.TYPES[1]

    @staticmethod
    def get_typeCoil():
        return Component.TYPES[2]

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def __str__(self):
        return f"{self.get_name()}={self.parameter}"
