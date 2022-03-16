import math
from network.component import Component

def calculateOrientation(direction):
    rx = (0+abs(direction))%2
    ry = (1+abs(direction))%2
    dirx = 1
    diry = 1
    if direction == 2:
        dirx = -1.0
    elif direction == 3:
        diry = -1.0
    return rx, ry, dirx, diry

class DrawElement:
    def __init__(self, source, size, direction, scale, type):
        self.x = source[0]
        self.y = source[1]
        self.size = size
        self.wirethickness = size *0.02
        self.type = type
        self.scale = scale
        self.orientation = calculateOrientation(direction)
        self.text = ""

    '''
    Get Key
    '''
    def generateKey(self):
        return str(self.x)+"-"+str(self.y)

    '''
    Get Type
    '''
    def getType(self):
        return self.type

    '''
    Set Text
    '''
    def setText(self, text):
        self.text = text

    '''
    Get Text
    '''
    def getText(self):
        return self.text

    '''
    Get start position of the component
    '''
    def getStart(self):
        return (self.x, self.y)

    '''
    Get end position of the component
    '''
    def getEnd(self):
        hsize = 0
        vsize = 0
        if self.type != "N":
            if self.orientation[0] == 0:
                hsize = self.orientation[2] * self.size * self.scale
            if self.orientation[1] == 0:
                vsize = self.orientation[3] * self.size * self.scale

        return (self.x + hsize, self.y + vsize)

    '''
    Get polygons
    '''
    def getPolygons(self):
        # Calculate wire points
        polygons = []
        if self.type == "W":
            wire = []
            wire.append([0, (self.wirethickness)/2*self.scale])
            wire.append([self.size*self.scale, self.wirethickness/2*self.scale])
            wire.append([self.size*self.scale, -self.wirethickness/2*self.scale])
            wire.append([0, -self.wirethickness/2*self.scale])
            polygons.append(wire)

        elif self.type == "N":
            node = []
            size = self.wirethickness * 2
            node.append([- size*self.scale, -size*self.scale])
            node.append([size*self.scale,  -size*self.scale])
            node.append([size*self.scale, size*self.scale])
            node.append([-size*self.scale, size*self.scale])
            polygons.append(node)

        elif self.type == Component.getTypeCoil():
            con1 = []
            con1.append([0, self.wirethickness/2])
            con1.append([self.size*0.2, self.wirethickness/2])
            con1.append([self.size*0.2, -self.wirethickness/2])
            con1.append([0, -self.wirethickness/2])

            con2 = []
            con2.append((self.size*0.8, self.wirethickness/2))
            con2.append((self.size, self.wirethickness/2))
            con2.append((self.size, -self.wirethickness/2))
            con2.append((self.size*0.8, -self.wirethickness/2))

            part_a = []
            part_a.append((self.size*0.2, self.size*0.12))
            part_a.append((self.size*0.8, self.size*0.12))
            part_a.append((self.size*0.8, -self.size*0.12))
            part_a.append((self.size*0.2, -self.size*0.12))

            # polygons
            polygons.append(con1)
            polygons.append(con2)
            polygons.append(part_a)
        elif self.type == Component.getTypeResistor():
            con1 = []
            con1.append([0, self.wirethickness/2])
            con1.append([self.size*0.2, self.wirethickness/2])
            con1.append([self.size*0.2, -self.wirethickness/2])
            con1.append([0, -self.wirethickness/2])

            con2 = []
            con2.append((self.size*0.8, self.wirethickness/2))
            con2.append((self.size, self.wirethickness/2))
            con2.append((self.size, -self.wirethickness/2))
            con2.append((self.size*0.8, -self.wirethickness/2))

            part_a = []
            part_a.append((self.size*0.2, self.size*0.12))
            part_a.append((self.size*0.8, self.size*0.12))
            part_a.append((self.size*0.8, -self.size*0.12))
            part_a.append((self.size*0.2, -self.size*0.12))

            # polygons
            polygons.append(con1)
            polygons.append(con2)
            polygons.append(part_a)
        elif self.type == Component.getTypeCapacitor():
            con1 = []
            con1.append([0, self.wirethickness/2])
            con1.append([self.size*0.2, self.wirethickness/2])
            con1.append([self.size*0.2, -self.wirethickness/2])
            con1.append([0, -self.wirethickness/2])

            con2 = []
            con2.append((self.size*0.8, self.wirethickness/2))
            con2.append((self.size, self.wirethickness/2))
            con2.append((self.size, -self.wirethickness/2))
            con2.append((self.size*0.8, -self.wirethickness/2))

            part_a = []
            part_a.append((self.size*0.2, self.wirethickness/2))
            part_a.append((self.size*0.4, self.wirethickness/2))
            part_a.append((self.size*0.4, self.size*0.24))
            part_a.append((self.size*0.45, self.size*0.24))
            part_a.append((self.size*0.45, -self.size*0.24))
            part_a.append((self.size*0.4, -self.size*0.24))
            part_a.append((self.size*0.4, -self.wirethickness/2))
            part_a.append((self.size*0.2, -self.wirethickness/2))

            part_b = []
            part_b.append((self.size*0.8, self.wirethickness/2))
            part_b.append((self.size*0.6, self.wirethickness/2))
            part_b.append((self.size*0.6, self.size*0.24))
            part_b.append((self.size*0.55, self.size*0.24))
            part_b.append((self.size*0.55, -self.size*0.24))
            part_b.append((self.size*0.6, -self.size*0.24))
            part_b.append((self.size*0.6, -self.wirethickness/2))
            part_b.append((self.size*0.8, -self.wirethickness/2))

            # polygons
            polygons.append(con1)
            polygons.append(con2)
            polygons.append(part_a)
            polygons.append(part_b)
        # Rotate
        for idx in range(len(polygons)):
            shape = polygons[idx]
            for idy in range(len(shape)):
                polygons[idx][idy] = (self.x + self.orientation[2] * shape[idy][self.orientation[0]], self.y + self.orientation[3] * shape[idy][self.orientation[1]])

        return polygons
