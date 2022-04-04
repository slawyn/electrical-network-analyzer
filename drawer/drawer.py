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
    COMPONENT_SCALE = 1
    OFFSET_START = (COMPONENT_SIZE, COMPONENT_SIZE+(CANVAS_SIZE_Y-COMPONENT_SIZE*2)/2)

    # color
    COLOR_TEXT = (0xFF, 0, 0)
    COLOR_WIRE = (0xFF,0x88,0x88)
    COLOR_NODE = (0xFF,0x60,0)
    COLOR_COMPONENT = (0,0,0)
    COLOR_BACKGROUND = (255,255,255)


    '''
    Constructor
    '''
    def __init__(self, network):
        self.network = network
        self.imagename = "%s.png"%str(self.network.getNetworkName())

        self.image = Image.new("RGB",(int(NetworkDrawer.CANVAS_SIZE_X),int(NetworkDrawer.CANVAS_SIZE_Y)),color=NetworkDrawer.COLOR_BACKGROUND)
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype("arial.ttf", 14)

        self.map = {}
        self.tkImage = None


        # drawing configuration
        scale = NetworkDrawer.COMPONENT_SCALE
        self.cftilesize = NetworkDrawer.COMPONENT_SIZE*scale
        self.cfoffset = NetworkDrawer.OFFSET_START*scale

        self.cfblockscntx = (NetworkDrawer.CANVAS_SIZE_X-self.cftilesize*2)/self.cftilesize
        self.cfblockscnty = (NetworkDrawer.CANVAS_SIZE_Y-self.cftilesize*2)/self.cftilesize


    '''
    Main method
    '''
    def drawNetwork(self):
        log("########## Network Drawer #############")
        debug = 0
        if debug == 0:
            # Calculate longest path
            nodes = self.network.getSortedNodes()

            # Save graphical connections
            conn_sources = {}
            conn_destinations = {}
            for node in nodes:
                conn_destinations[node.name] = []


            # Generate components and nodes
            source = self.cfoffset
            for snode in nodes:
                len_comps = len(snode.components)

                # Node
                e_start = (source[0], source[1])
                e = DrawElement(e_start, self.cftilesize, 0, "N", snode.name)
                #self.addToMap(e)

                # collect connections
                conn_sources[snode.name] = e_start

                # Positions
                y = source[1] - ((len_comps-1) * self.cftilesize)
                source = (e_start[0] + self.cftilesize, source[1])

                # Components
                for tnode in snode.components:
                    for comp in snode.components[tnode]:

                        # element
                        e_start = (source[0], y)
                        e_end = (source[0] + self.cftilesize, y)

                        e = DrawElement(e_start, self.cftilesize, 0, comp.getType(), comp.getIdentifier())
                        self.addToMap(e)

                        # nodes
                        try:
                            conn_destinations[snode.name].append(e_start)
                            conn_destinations[tnode].append(e_end)
                        except:
                            raise ValueError("Error: Network cannot be drawn. Not connection between nodes %s"%snode.name)

                        y += self.cftilesize

                source = (e_start[0] + self.cftilesize*2, source[1])

            # Generate Connections
            for n in conn_sources:
                #log("[%s]%s->%s"%(n, conn_sources[n], str(conn_destinations[n])))
                dests = conn_destinations[n]
                for d in dests:
                    self.addPathBetweenPoints(conn_sources[n], d)
        else:
            self.generateTestMap1()

        # Draw
        self.drawMap()
        self.showInPanel()


    '''
    Connect points
    '''
    def addPathBetweenPoints(self, source, destination):
        dx = 0
        dy = 0
        x = 0
        y = 0

        # define priorities
        if source[0]>destination[0]:
            dx = -1
        elif source[0]>destination[0]:
            dx = 1
        if source[1]>destination[1]:
            dy = -1
        elif source[1]<destination[1]:
            dy = 1

        x = source[0]-destination[0]
        y = source[1]-destination[1]


        e = DrawElement((source[0], source[1]), x, 0, "W", "")
        self.addToMap(e)

        e = DrawElement((source[0]+x, source[1]), y, 0, "W", "")
        self.addToMap(e)
        '''
        while True:
            if (y + self.cftilesize*dy):
                pass

            if (x + self.cftilesize*dx):
                pass
        '''

    '''
    debug map
    '''
    def generateTestMap1(self):
        source = self.cfoffset
        element = DrawElement(source, self.cftilesize, 0, "N")
        self.addToMap(element)

        element = DrawElement(source, self.cftilesize, 0, "W")
        self.addToMap(element)

        element = DrawElement(element.getEnd(), self.cftilesize, 1, "L")
        self.addToMap(element)

        element = DrawElement(element.getEnd(), self.cftilesize, 1, "C")
        self.addToMap(element)

        element = DrawElement(element.getEnd(), self.cftilesize, 0, "R")
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


    '''
    Save drawn network image to disk
    '''
    def saveImage(self):
        self.image.save(os.path.join(NetworkDrawer.DIRECTORY, self.imagename ))

    '''
    Add to map
    '''
    def addToMap(self, element):
        xy = self.getBlock(element.getStart())
        if xy in self.map:
            self.map[xy].append(element)
        else:
            self.map[xy] = [element]

    '''

    '''
    def getBlock(self, position):
        return str(position[0]) + "-" + str(position[1])

    def isBlockInUse(self, position):
        xy = self.getBlock(position)
        if xy in self.map:
            return True
        else:
            return False


    '''
    Draw generated list of elements
    '''
    def drawMap(self):
        log("Elements:")
        for xy in self.map:
            for e in self.map[xy]:
                log("[%s] %s"%(e.getType(),e.getStart()))

        for xy in self.map:
            for e in self.map[xy]:
                self.drawElement(e)

    '''
    Draw Element from map
    '''
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
