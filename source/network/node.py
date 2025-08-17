
class Connection:
    def __init__(self, name, node1, node2):
        self.name = name
        self.snode, self.enode = node1, node2
        self.phaseshift = 0
        self.impedance = 0
        self.components = []
        self.snode.add_connection(self)
        self.enode.add_connection(self)

    def get_name(self):
        return self.name

    def get_connecting_node(self, node):
        if node == self.snode:
            return self.enode
        return self.snode

    def get_nodes(self):
        return self.snode, self.enode

    def add_component(self, component):
        self.components.append(component)

    def get_components(self):
        return self.components

    def set_properties(self, impedance, phaseshift):
        self.impedance = impedance
        self.phaseshift = phaseshift

    def get_properties(self):
        return self.impedance, self.phaseshift


class Node:
    def __init__(self, name):
        self.name = name
        self.depthscore = 0
        self.type = "N"
        self.connections = []

    def add_connection(self, connection):
        self.connections.append(connection)

    def get_connections(self):
        return self.connections

    def set_depth(self, depth):
        self.depthscore = depth

    def get_type(self):
        return self.type

    def get_depth(self):
        return self.depthscore

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name
