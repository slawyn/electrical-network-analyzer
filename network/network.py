from helpers import log, cmp, readfile, getfilename
from network.component import Component
from network.node import Node

#external dependencies
import math
from functools import cmp_to_key

class Network:
    def __init__(self, filepath):
        self.nodes_table = {}
        self.nodes_ref = []
        self.nodes_sorted_levels = []

        self.variables = {}
        self.frequency = 1
        self.refs = []
        self.networkname = ""

        # Load network from file
        self.loadNetworkFromFile(filepath)

    def getFrequency(self):
        return self.frequency

    def createNode(self, key):
        node = Node(key)
        self.nodes_table[node.name] = node
        return node

    def findNode(self, key):
        if key in self.nodes_table:
            return self.nodes_table[key]
        else:
            return None

    def addComponent(self, startnode, endnode, component):

        # Sort for ease of parsing, because it does not have influence on passive components
        # Sort the nodes priortizing reference "a", "b". "a" should be one of the sources and "b" should be in one of the endpoints
        # Otherwise sort alphabetically
        if endnode == self.nodes_ref[0].name or startnode == self.nodes_ref[1].name or 1 == cmp(startnode, endnode):
            t = startnode
            startnode = endnode
            endnode = t

        # Find if one of the nodes exist. Then add component between nodes
        source = self.findNode(startnode)
        sink = self.findNode(endnode)

        if source != None and sink != None:
            source.addComponentBetweenNodes(sink, component)
        elif source!=None:
            source.addComponentBetweenNodes(self.createNode(endnode), component)

        # Create both
        else:
            node0 = self.createNode(startnode)
            node1 = self.createNode(endnode)
            node0.addComponentBetweenNodes(node1, component)

    # load network and vars from file
    def loadNetworkFromFile(self, filepath):
        self.networkname = getfilename(filepath)

        # read file
        for line in readfile(filepath):
            args = line.split()
            if len(args)>0:
                if '#' not in args[0]:  # lines with # are commented out
                    if args[0] == "freq":
                        freq = float(args[1])
                        if freq == 0:
                            log("Warning. Frequency cannot be 0. Setting it to 1")
                        self.frequency = freq
                    elif args[0] == "var":
                        name  = args[1]
                        value = float(args[2])
                        self.variables[name] = value

                    elif args[0] == "ref":
                        if len(self.nodes_ref) == 0:
                            self.nodes_ref.append(self.createNode(args[1]))
                            self.nodes_ref.append(self.createNode(args[2]))
                        else:
                            log("Warning. ref should only be defined once. Ignoring redefinitions")

                    elif args[0] == "comp":
                        if args[1] == args[2]:
                            log("Warning. Component %s on node %s is shorted to self and will be removed."%(args[3], args[1]))
                        else:
                            value = 0
                            if args[4].isnumeric():
                                value = float(args[4])
                            #variable
                            else:
                                value = self.variables[args[4]]
                            self.addComponent(args[1], args[2], Component(args[1]+"_"+args[2], args[3], value))

        # Validate the network
        # 1. validate that there is atleast one path between the references
        if not self.getPathBetweenReferences():
            raise ValueError("Error: Network is not valid. Path between references has not been defined.")

        self.generateAdditionalInformation()

    '''
    Additional post processing of the structure
    '''
    def generateAdditionalInformation(self):
         # Calculate depth
        self.nodes_ref[0].calculateNodesDepth(self.nodes_ref[1])
        self.nodes_sorted_levels = list(self.nodes_table.values())
        self.nodes_sorted_levels.sort(key=cmp_to_key(lambda item1, item2: item1.getDepthScore() - item2.getDepthScore()))

    def getPathBetweenReferences(self):
        return self.nodes_ref[0].findPathToNode(self.nodes_ref[1])

    def getLongestNetworkPath(self):
        path = self.nodes_ref[0].findLongestPathToNode(self.nodes_ref[1])
        ostring = self.nodes_ref[0].getName()+"->"
        for p in path:
            ostring+=p.getName()+"->"
        ostring +=self.nodes_ref[1].getName()
        return ostring

    def getNetworkName(self):
        return self.networkname

    def getSortedNodes(self):
        return self.nodes_sorted_levels

    # Print contents of network
    def printContents(self):
        log("########## Network Analyzer #############")
        log("Name: %s"%(self.networkname))
        log("Ref. Nodes: [%s->%s]"%(str(self.nodes_ref[0]),str(self.nodes_ref[1])))
        log("Frequency[Hz]: %f"%(self.frequency))
        log("Variables: %s"%str(self.variables))
        log("-Longestpath: [%s]"%(self.getLongestNetworkPath()))
        log("-Connections:level.[a->b]{components}")
        for node in self.nodes_sorted_levels:
            for c in node.components:
                parallel_comps = ""
                for comp in  node.components[c]:
                    parallel_comps = parallel_comps +comp.identifier + " "
                log(" *%d.[%-3s->%-3s]  Z[Ohm]: %-15f\tPhi[Deg]: %-f "%(node.depthscore, node.name, c, node.impedance[c],node.phaseshift[c]))
                log(" %-s"%parallel_comps)
