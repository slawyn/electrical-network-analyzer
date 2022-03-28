from helpers import log
from network.component import Component
from drawer.elements import DrawElement

#external dependencies
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk


class NetworkDrawer():
    DIRECTORY = "output-analysis"
    CANVAS_SIZE_Y = 1080.0
    CANVAS_SIZE_X = 1920.0
    UNIT = 10

    COMPONENT_SIZE  = 12 * UNIT       # GCD 12
    COMPONENT_NODE = COMPONENT_SIZE * 0.1

    COLOR_TEXT = (0xFF, 0, 0)
    COLOR_WIRE = (0xFF,0x88,0x88)
    COLOR_NODE = (0xFF,0x60,0)
    COLOR_COMPONENT = (0,0,0)
    COLOR_BACKGROUND = (255,255,255)

    OFFSET_START = (COMPONENT_SIZE, COMPONENT_SIZE+(CANVAS_SIZE_Y-COMPONENT_SIZE*2)/2)

    def __init__(self, network):
        self.network = network
        self.imagename = "%s.png"%str(self.network.getNetworkName())

        self.image = Image.new("RGB",(int(NetworkDrawer.CANVAS_SIZE_X),int(NetworkDrawer.CANVAS_SIZE_Y)),color=NetworkDrawer.COLOR_BACKGROUND)
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype("arial.ttf", 14)

        self.map = {}
        self.scale = 1
        self.tkImage = None

    '''
    Main method
    '''
    def drawNetwork(self):

        #self.generateTestMap0()
        log("########## Network Drawer #############")
        # find the right scale for the network x
        count_available_x = (NetworkDrawer.CANVAS_SIZE_X-NetworkDrawer.COMPONENT_SIZE*2)/NetworkDrawer.COMPONENT_SIZE
        count_available_y = (NetworkDrawer.CANVAS_SIZE_Y-NetworkDrawer.COMPONENT_SIZE*2)/NetworkDrawer.COMPONENT_SIZE

        # Calculate longest path
        nodes = self.network.getSortedNodes()

        # save graphical connections
        conn_sources = {}
        conn_destinations = {}
        for node in nodes:
            conn_destinations[node.name] = []

        # Generate components
        source = NetworkDrawer.OFFSET_START
        for snode in nodes:
            len_comps = len(snode.components)

            # Node
            element_start = (source[0] + NetworkDrawer.COMPONENT_SIZE + NetworkDrawer.COMPONENT_SIZE/2, source[1])
            e = DrawElement( element_start, NetworkDrawer.COMPONENT_SIZE, 0, self.scale, "N")
            e.setText(snode.name)
            self.addToMap(e)

            # collect connections
            conn_sources[snode.name] = element_start

            # Positions
            y = source[1] - ((len_comps-1) * NetworkDrawer.COMPONENT_SIZE)
            source = (source[0]+ NetworkDrawer.COMPONENT_SIZE*2, source[1])

            # Components
            for tnode in snode.components:
                for comp in snode.components[tnode]:

                    # element
                    e_start =  (source[0], y)
                    e_end = (source[0] + NetworkDrawer.COMPONENT_SIZE, y)
                    e = DrawElement(e_start, NetworkDrawer.COMPONENT_SIZE, 0, self.scale, comp.getType())
                    e.setText(comp.identifier)
                    self.addToMap(e)

                    # nodes
                    try:
                        conn_destinations[snode.name].append(e_start)
                        conn_destinations[tnode].append(e_end)
                    except:
                        raise ValueError("Error: Network is not valid. Path between references has not been defined.")

                    y += NetworkDrawer.COMPONENT_SIZE


        log("Elements:")
        for xy in self.map:
            for element in self.map[xy]:
                log("[%s] %s"%(element.getType(),element.getStart()))

        # Connections
        log("Connections:")
        for n in conn_sources:
            log("[%s]%s->%s"%(n, conn_sources[n], str(conn_destinations[n])))

        # Draw connections
        self.drawMap()
        self.showInPanel()

    def drawPathBetweenPoints(source, destination):
        pass

    def generateTestMap0(self):
        source = NetworkDrawer.OFFSET_START
        element = DrawElement(source, NetworkDrawer.COMPONENT_SIZE, 0, self.scale, "N")
        self.addToMap(element)

        element = DrawElement(source, NetworkDrawer.COMPONENT_SIZE, 0, self.scale, "W")
        self.addToMap(element)

        element = DrawElement(element.getEnd(), NetworkDrawer.COMPONENT_SIZE, 1, self.scale, "L")
        self.addToMap(element)

        element = DrawElement(element.getEnd(), NetworkDrawer.COMPONENT_SIZE, 1, self.scale, "C")
        self.addToMap(element)

        element = DrawElement(element.getEnd(), NetworkDrawer.COMPONENT_SIZE, 0, self.scale, "R")
        self.addToMap(element)

    '''
    Show drawn network in panel
    Create tkinter preview
    '''
    def showInPanel(self):

        base = tk.Tk()
        base.title(self.imagename)

        pawin = tk.PanedWindow(orient ='vertical')
        button = tk.Button (base, text=  "Save Image", command=self.saveImage)
        button.pack()

        self.tkImage = ImageTk.PhotoImage(self.image)
        label = tk.Label(image = self.tkImage)
        label.pack(side = 'top')
        base.mainloop()

    # Save drawn network image to disk
    def saveImage(self):
        self.image.save(os.path.join(NetworkDrawer.DIRECTORY, self.imagename ))

    def addToMap(self, element):
        xy = element.generateKey()
        if xy in self.map:
            self.map[xy].append(element)
        else:
            self.map[xy] = [element]

    '''
    Draw generated list of elements
    '''
    def drawMap(self):
        for xy in self.map:
            for element in self.map[xy]:
                self.drawElement(element)

    def drawElement(self, element):
        polygons = element.getPolygons()
        start = element.getStart()
        text = element.getText()
        for idx in range(len(polygons)):
            shape = polygons[idx]
            if element.getType() == "W":
                self.draw.polygon(shape, fill = NetworkDrawer.COLOR_WIRE)
            elif element.getType() == "N":
                self.draw.polygon(shape, fill = NetworkDrawer.COLOR_NODE)
            elif element.getType() == "L" or element.getType() == "C":
                self.draw.polygon(shape, fill = NetworkDrawer.COLOR_COMPONENT)
            elif element.getType() == "R":
                self.draw.polygon(shape, outline = NetworkDrawer.COLOR_COMPONENT)

        self.draw.text((start[0]+3, start[1]+3), text, NetworkDrawer.COLOR_TEXT, font=self.font)
