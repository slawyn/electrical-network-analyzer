import math
from source.network.component import Component


def rotatePolygon(polygons, x_pos, y_pos, degrees):
    theta = math.radians(degrees)
    cos_theta, sin_theta = math.cos(theta), math.sin(theta)

    rotated_polygons = []
    for shape in polygons:
        rotated_shape = []
        for x, y in shape:
            # Translate point to origin
            tx, ty = x, y

            # Apply rotation
            new_x = (tx * cos_theta - ty * sin_theta)
            new_y = (tx * sin_theta + ty * cos_theta)

            # Translate point back
            rotated_x = new_x + x_pos
            rotated_y = new_y + y_pos

            rotated_shape.append((rotated_x, rotated_y))
        rotated_polygons.append(rotated_shape)
    return rotated_polygons


def calculateDistance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx**2 + dy**2)


def calculateAngle(x1, y1, x2, y2):
    vx = x2 - x1
    vy = y2 - y1

    # Use atan2 to get the signed angle in radians
    # atan2(y, x) gives the angle relative to the positive x-axis
    angle_rad = math.atan2(vy, vx)

    # Convert from radians to degrees
    angle_deg = math.degrees(angle_rad)
    return angle_deg


class Drawable:
    def __init__(self, source, size, angle, type, label=""):
        self.x1, self.y1 = source[0], source[1]
        self.size = size
        self.angle = angle
        self.wirethickness = self.size * 0.02
        self.type = type
        self.name = label

    def update_position(self, x, y):
        self.x1, self.y1 = x, y

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def getStart(self):
        return (self.x1, self.y1)

    def getAngle(self):
        return self.angle

    def getPolygons(self):
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
            size = wirethickness * 2
            rombus = []
            rombus.append((-size*2, 0))
            rombus.append((0, -size*2))
            rombus.append((size*2, 0))
            rombus.append((0, size*2))
            polygons.append(rombus)

        elif self.type == Component.get_typeCoil():
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
        elif self.type == Component.get_typeResistor():
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
        elif self.type == Component.get_typeCapacitor():
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

        return rotatePolygon(polygons, self.x1, self.y1, self.angle)
