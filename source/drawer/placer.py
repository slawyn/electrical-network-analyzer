import math
import random
from collections import deque
from typing import List, Dict, Tuple, Set

from source.drawer.drawable import Drawable


class Placer:
    """
    A class to handle the logical placement of nodes and components in a network layout.
    It separates the layout logic from the drawing and rendering.
    """

    def __init__(self, cftilesize: float, cfcomponentsize: float, xcount: int, ycount: int):
        self.cftilesize = cftilesize
        self.cfcomponentsize = cfcomponentsize
        self.xcount = xcount
        self.ycount = ycount
        self.convergence_threshold = cftilesize

    def _initial_placement(self, network) -> Tuple[List, Dict, Dict, Dict]:
        """
        Places nodes and components on a grid to ensure no initial overlaps.
        """
        elements_to_draw = []
        node_positions = {}
        component_positions = {}
        component_to_nodes = {}

        # Consolidate all unique elements (nodes and components)
        unique_elements = self._get_unique_elements(network)

        # Grid-based placement
        grid_pos = 0
        for element in unique_elements:
            element_type = element.get_type()
            element_name = element.get_name()

            # Calculate grid coordinates
            col = grid_pos % self.xcount
            row = grid_pos // self.xcount

            x = col * self.cftilesize
            y = row * self.cftilesize

            new_drawable = Drawable(
                [x, y],
                self.cfcomponentsize,
                angle=0,
                type=element_type,
                label=element_name
            )
            elements_to_draw.append(new_drawable)

            if element_type == "N":
                node_positions[element_name] = [x, y]
            else:
                component_positions[element_name] = [x, y]

            grid_pos += 1
            if grid_pos >= self.xcount * self.ycount:
                # Handle overflow if more elements than grid cells
                break

        # Build the component_to_nodes mapping from the network structure
        for node in network.get_sorted_nodes():
            for connection in node.get_connections():
                for component in connection.get_components():
                    comp_name = component.get_name()
                    if comp_name not in component_to_nodes:
                        component_to_nodes[comp_name] = []
                    component_to_nodes[comp_name].append(node.get_name())

        return elements_to_draw, node_positions, component_positions, component_to_nodes

    def _get_unique_elements(self, network):
        """Helper to collect all unique nodes and components from the network."""
        unique_elements = {}
        for node in network.get_sorted_nodes():
            unique_elements[node.get_name()] = node

        for node in network.get_sorted_nodes():
            for connection in node.get_connections():
                for component in connection.get_components():
                    unique_elements[component.get_name()] = component

        # Return as a list to maintain order if desired, or as a random set
        return list(unique_elements.values())

    def place(self, network):
        max_iterations = 100
        learning_rate = 0.0001
        attraction_strength = 0.5

        # New constants for repulsion and margin
        repulsion_strength = 1000  # Increased for stronger repulsion
        margin = self.cftilesize
        min_dist_sq = (self.cfcomponentsize + margin) ** 2

        # A set to keep track of all elements that are already placed
        elements_to_draw, node_positions, component_positions, component_to_nodes = self._initial_placement(network)
        placed_elements_names = set(node_positions.keys())

        # Use a queue for breadth-first processing of nodes
        nodes_to_process = deque(node_positions.keys())

        while nodes_to_process:
            current_node_name = nodes_to_process.popleft()

            # Get components connected to the current node that haven't been placed yet
            components_to_refine = [
                elem for elem in elements_to_draw
                if elem.type != "N" and current_node_name in component_to_nodes.get(elem.get_name(), [])
                and elem.get_name() not in placed_elements_names
            ]

            if not components_to_refine:
                continue

            # Add the newly refined components to the set of placed elements
            for comp in components_to_refine:
                placed_elements_names.add(comp.get_name())

            # Perform local force-directed optimization for the new components
            for _ in range(max_iterations):
                max_movement = 0
                new_positions = {}

                # Create a temporary list of all fixed positions (nodes and components already placed)
                fixed_positions = list(node_positions.values())
                fixed_positions.extend([component_positions[name]
                                       for name in placed_elements_names if name not in node_positions.keys()])

                for component_element in components_to_refine:
                    label = component_element.get_name()
                    current_x, current_y = component_positions[label]

                    attraction_x, attraction_y = 0, 0
                    repulsion_x, repulsion_y = 0, 0

                    # Attraction to connected nodes
                    for connected_element_name in component_to_nodes.get(label, []):
                        if connected_element_name in node_positions:
                            target_x, target_y = node_positions[connected_element_name]
                            dx = target_x - current_x
                            dy = target_y - current_y
                            attraction_x += dx * attraction_strength
                            attraction_y += dy * attraction_strength

                    # Repulsion from all fixed elements
                    for other_pos in fixed_positions:
                        dx = current_x - other_pos[0]
                        dy = current_y - other_pos[1]
                        dist_sq = dx**2 + dy**2

                        if dist_sq > 0 and dist_sq < min_dist_sq:
                            # Repulsion force
                            repulsion_factor = repulsion_strength / dist_sq
                            repulsion_x += dx * repulsion_factor
                            repulsion_y += dy * repulsion_factor

                    total_dx = (attraction_x + repulsion_x) * learning_rate
                    total_dy = (attraction_y + repulsion_y) * learning_rate

                    new_x = current_x + total_dx
                    new_y = current_y + total_dy

                    movement = math.sqrt(total_dx**2 + total_dy**2)
                    max_movement = max(max_movement, movement)
                    new_positions[label] = [new_x, new_y]

                # Update positions
                for label, pos in new_positions.items():
                    component_positions[label] = pos

                if max_movement < self.convergence_threshold:
                    break

            # Add newly connected nodes to the queue for future processing
            for comp in components_to_refine:
                for neighbor_node in component_to_nodes.get(comp.get_name(), []):
                    if neighbor_node not in placed_elements_names:
                        nodes_to_process.append(neighbor_node)

        # Final grid snapping for all elements
        for element in elements_to_draw:
            if element.get_name() in component_positions:  # Checks if the element is a component
                label = element.get_name()
                x, y = component_positions[label]
                grid_x = round(x / self.cftilesize) * self.cftilesize
                grid_y = round(y / self.cftilesize) * self.cftilesize
                element.update_position(grid_x, grid_y)
                component_positions[label] = [grid_x, grid_y]

        return elements_to_draw
