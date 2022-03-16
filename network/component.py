import math

class Component():
    TYPES = ["R","C","L"]
    COUNTERS = [0,0,0]

    def __init__(self, type, parameter):
        self.parameter = parameter
        self.type = type

        # Increment the components counter
        idx = Component.TYPES.index(type)
        if idx>=0:
            self.identifier = type + str(Component.COUNTERS[idx])
            Component.COUNTERS[idx]+=1
        else:
            raise ValueError("Error:Unknown component type")

    def getValue(self, frequency):
        Re, Im = 0, 0
        if self.type == Component.TYPES[0]:
            Re = self.parameter
        elif self.type == Component.TYPES[1]:
            Im =  (-1/(2*math.pi*self.parameter*frequency))
        else:
            Im = (2*math.pi*self.parameter*frequency)
        return Re, Im

    @staticmethod
    def getTypeResistor():
        return Component.TYPES[0]

    @staticmethod
    def getTypeCapacitor():
        return Component.TYPES[1]

    @staticmethod
    def getTypeCoil():
        return Component.TYPES[2]

    def getType(self):
        return self.type

    def getIdentifier(self):
        return self.identifier

    def __str__(self):
        return self.getIdentifier()
