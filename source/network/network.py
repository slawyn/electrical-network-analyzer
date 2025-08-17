import math
from functools import cmp_to_key

from source.helpers import log, cmp, readfile, getfilename
from source.network.component import Component
from source.network.node import Node, Connection


class ConnectionHelper:
    def __init__(self):
        self.visited = []

    def search(self, current, target):
        paths = []
        for connection in current.get_connections():
            name = connection.get_name()
            node = connection.get_connecting_node(current)
            if node in self.visited:
                pass
            else:
                if node == target:
                    paths.append([name])
                else:
                    self.visited.append(node)
                    if connections := self.search(node, target):
                        for connection in connections:
                            connection.insert(0, name)
                        paths.extend(connections)
                    self.visited.remove(node)
        return paths

    def calculate_depth(self, current, target, depth=0):
        if depth > current.get_depth():
            current.set_depth(depth)

        # Base case for the recursive call to stop at the target node
        if current == target:
            return

        # Add the current node to the visited list for this traversal branch
        # This prevents cycles in the current path.
        self.visited.append(current)

        # Recurse for all unvisited neighbors
        for connection in current.get_connections():
            node = connection.get_connecting_node(current)

            if node not in self.visited:
                # Recursively call the function for the next node with an increased depth
                self.calculate_depth(node, target, depth + 1)

        # Backtrack: Remove the current node from the visited list
        # This is crucial to allow other paths to visit this node
        self.visited.remove(current)


class Network:
    def __init__(self, filepath):
        self.nodes = {}
        self.connections = {}
        self.refs = []
        self.sorted = []

        self.variables = {}
        self.frequency = 1
        self.name = ""

        # Load network from file
        self.loadNetworkFromFile(filepath)

    def getFrequency(self):
        return self.frequency

    def getNode(self, key):
        if key in self.nodes:
            return self.nodes[key]
        else:
            node = Node(key)
            self.nodes[node.name] = node
            return node

    def addComponent(self, startnode, endnode, type, value):
        source = self.getNode(startnode)
        sink = self.getNode(endnode)

        if 1 == cmp(startnode, endnode):
            key = f"{endnode}-{startnode}"
        else:
            key = f"{startnode}-{endnode}"

        component = Component(key, type, value)
        if key in self.connections:
            connection = self.connections[key]
            connection.add_component(component)
        else:
            connection = Connection(key, source, sink)
            self.connections[key] = connection
            connection.add_component(component)

    def loadNetworkFromFile(self, filepath):
        self.name = getfilename(filepath)

        handlers = {
            "freq": self._handle_freq,
            "var": self._handle_var,
            "ref": self._handle_ref,
            "comp": self._handle_comp,
        }

        # read and process each line
        for line in readfile(filepath):
            args = line.split()
            if args and not args[0].startswith('#'):
                command = args[0]
                if command in handlers:
                    handlers[command](args)

        # The new validation and finalization steps
        # 1. Validate that there is at least one path between the references
        cp = ConnectionHelper()
        paths = cp.search(self.refs[0], self.refs[1])
        if not paths:
            raise Exception("No path found between")

        # 2. Generate additional information
        self.generateAdditionalInformation()

    def _handle_freq(self, args):
        freq = float(args[1])
        if freq == 0:
            log("Warning. Frequency cannot be 0. Setting it to 1")
        self.frequency = freq

    def _handle_var(self, args):
        name = args[1]
        value = float(args[2])
        self.variables[name] = value

    def _handle_ref(self, args):
        if not self.refs:
            self.refs.append(self.getNode(args[1]))
            self.refs.append(self.getNode(args[2]))
        else:
            log("Warning. ref should only be defined once. Ignoring redefinitions")

    def _handle_comp(self, args):
        if args[1] == args[2]:
            log(f"Warning. Component {args[3]} on node {args[1]} is shorted to self and will be removed.")
        else:
            value = float(self.variables[args[4]] if not args[4].isnumeric() else args[4])
            self.addComponent(args[1], args[2],  args[3], value)

    def generateAdditionalInformation(self):
        ch = ConnectionHelper()
        ch.calculate_depth(self.refs[0],  self.refs[1])
        for key, node in self.nodes.items():
            log(f"{key}: {node.get_depth()}")
        self.sorted = list(self.nodes.values())
        self.sorted.sort(key=cmp_to_key(lambda item1, item2: item1.get_depth() - item2.get_depth()))

    def get_name(self):
        return self.name

    def get_sorted_nodes(self):
        return self.sorted

    def get_connections(self):
        return self.connections.values()

    # Print contents of network
    def printContents(self):
        log("Name: %s" % (self.name))
        log("Ref. Nodes: [%s->%s]" % (str(self.refs[0]), str(self.refs[1])))
        log("Frequency[Hz]: %f" % (self.frequency))
        log("Variables: %s" % str(self.variables))
        log("Connections:level.[a->b]{components}")
        for key, connection in self.connections.items():
            components = " ".join([str(component) for component in connection.get_components()])
            impedance, phaseshift = connection.get_properties()

            node1, node2 = connection.get_nodes()
            log(f" {key:10}({node1.get_depth()}, {node2.get_depth()}) {components:30} Z={impedance:10.3f} Deg={phaseshift}")
