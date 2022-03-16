
class Node:
    def __init__(self, name):
        self.name = name
        self.previous = []
        self.next = []
        self.components = {}
        self.impedance = {}
        self.phaseshift = {}
        self.depthscore = 0

    def getDepthScore(self):
        return self.depthscore

    def addComponentBetweenNodes(self, node, component):
        if node not in self.next:
            self.next.append(node)
            node.previous = self

        if node.name not in self.components:
            self.components[node.name] = [component]
        else:
            self.components[node.name].append(component)

    def setProperties(self, ntn, impedance, phaseshift):
        self.impedance[ntn] = impedance
        self.phaseshift[ntn] = phaseshift

    def getComponents(self):
        return self.components

    '''
    Find the longest path to node and save the journey
    '''
    def findLongestPathToNode(self, endnode, path=[]):
        farthest_path = []
        for nxt in self.next:
            if nxt == endnode:
                if len(farthest_path) == 0:
                    farthest_path = path
            else:
                reached= nxt.findLongestPathToNode(endnode, path+[nxt])
                if len(reached)>len(farthest_path):
                    farthest_path = reached

        return farthest_path

    '''
    Find the atleast one path to node to validate the network
    '''
    def findPathToNode(self, endnode):
        found = False
        for nxt in self.next:
            if nxt == endnode:
                found = True
            else:
                found = nxt.findPathToNode(endnode)
            if found:
                break
        return found

    def getName(self):
        return self.name

    # Put all nodes on the level
    def calculateNodesDepth(self, endnode, depthcounter):
        for nxt in self.next:
            if depthcounter>nxt.depthscore:
                nxt.depthscore =depthcounter
            nxt.calculateNodesDepth(endnode, depthcounter+1)

    def __str__(self):
        return self.name
