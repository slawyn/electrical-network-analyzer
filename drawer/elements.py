import math
from network.component import Component

def rotatePolygon(polygons, x_pos, y_pos, degrees):
    """ Rotate polygon the given angle about its center. """
    theta = degrees/360*(2*math.pi)  # Convert angle to radians
    cosang, sinang = math.cos(theta), math.sin(theta)

    # points
    n = 0
    cx = 0
    cy = 0
    for shape in polygons:
        for p in shape:
            cx +=p[0]
            cy +=p[1]
            n +=1

    if n == 0:
        n = 1

    cx = cx/n
    cy = cy/n

    new_polygons = []
    for shape in polygons:
        new_shape = []
        for p in shape:
            x, y = p[0], p[1]
            tx, ty = x-cx, y-cy
            new_x = ( tx*cosang + ty*sinang) + cx
            new_y = (-tx*sinang + ty*cosang) + cy
            new_shape.append((new_x+x_pos, new_y+y_pos))
        new_polygons.append(new_shape)
    return new_polygons


class DrawElement:
    def __init__(self, source, size, angle, type, text=""):
        self.x = source[0]
        self.y = source[1]
        self.size = size
        self.wirethickness = size *0.02
        self.type = type
        self.angle = angle
        self.text = text

    '''
    Get Type
    '''
    def getType(self):
        return self.type

    '''
    Get Text
    '''
    def getText(self):
        return self.text

    '''
    Set Text
    '''
    def setText(self, text):
        self.text = text

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
                hsize = self.orientation[2] * self.size
            if self.orientation[1] == 0:
                vsize = self.orientation[3] * self.size

        return (self.x + hsize, self.y + vsize)

    '''
    Get polygons
    '''
    def getPolygons(self):
        # Calculate wire points
        polygons = []
        wirethickness = self.wirethickness
        size = self.size
        if self.type == "W":
            wire = []
            wire.append((0, (wirethickness)/2))
            wire.append((size, wirethickness/2))
            wire.append((size, -wirethickness/2))
            wire.append((0, -wirethickness/2))
            polygons.append(wire)

        elif self.type == "N":
            node = []
            size = wirethickness * 2
            node.append((- size, -size))
            node.append((size,  -size))
            node.append((size, size))
            node.append((-size, size))
            polygons.append(node)

        elif self.type == Component.getTypeCoil():
            con1 = []
            con1.append((0, wirethickness/2))
            con1.append((size*0.2, wirethickness/2))
            con1.append((size*0.2, -wirethickness/2))
            con1.append((0, -wirethickness/2))

            con2 = []
            con2.append((size*0.8, wirethickness/2))
            con2.append((size, wirethickness/2))
            con2.append((size, -wirethickness/2))
            con2.append((size*0.8, -wirethickness/2))

            part_a = []
            part_a.append((size*0.2, size*0.12))
            part_a.append((size*0.8, size*0.12))
            part_a.append((size*0.8, -size*0.12))
            part_a.append((size*0.2, -size*0.12))

            # polygons
            polygons.append(con1)
            polygons.append(con2)
            polygons.append(part_a)
        elif self.type == Component.getTypeResistor():
            con1 = []
            con1.append((0, wirethickness/2))
            con1.append((size*0.2, wirethickness/2))
            con1.append((size*0.2, -wirethickness/2))
            con1.append((0, -wirethickness/2))

            con2 = []
            con2.append((size*0.8, wirethickness/2))
            con2.append((size, wirethickness/2))
            con2.append((size, -wirethickness/2))
            con2.append((size*0.8, -wirethickness/2))

            part_a = []
            part_a.append((size*0.2, size*0.12))
            part_a.append((size*0.8, size*0.12))
            part_a.append((size*0.8, -size*0.12))
            part_a.append((size*0.2, -size*0.12))

            # polygons
            polygons.append(con1)
            polygons.append(con2)
            polygons.append(part_a)
        elif self.type == Component.getTypeCapacitor():
            con1 = []
            con1.append((0, wirethickness/2))
            con1.append((size*0.2, wirethickness/2))
            con1.append((size*0.2, -wirethickness/2))
            con1.append((0, -wirethickness/2))

            con2 = []
            con2.append((size*0.8, wirethickness/2))
            con2.append((size, wirethickness/2))
            con2.append((size, -wirethickness/2))
            con2.append((size*0.8, -wirethickness/2))

            part_a = []
            part_a.append((size*0.2, wirethickness/2))
            part_a.append((size*0.4, wirethickness/2))
            part_a.append((size*0.4, size*0.24))
            part_a.append((size*0.45, size*0.24))
            part_a.append((size*0.45, -size*0.24))
            part_a.append((size*0.4, -size*0.24))
            part_a.append((size*0.4, -wirethickness/2))
            part_a.append((size*0.2, -wirethickness/2))

            part_b = []
            part_b.append((size*0.8, wirethickness/2))
            part_b.append((size*0.6, wirethickness/2))
            part_b.append((size*0.6, size*0.24))
            part_b.append((size*0.55, size*0.24))
            part_b.append((size*0.55, -size*0.24))
            part_b.append((size*0.6, -size*0.24))
            part_b.append((size*0.6, -wirethickness/2))
            part_b.append((size*0.8, -wirethickness/2))

            # polygons
            polygons.append(con1)
            polygons.append(con2)
            polygons.append(part_a)
            polygons.append(part_b)

        return rotatePolygon(polygons, self.x, self.y, self.angle)
