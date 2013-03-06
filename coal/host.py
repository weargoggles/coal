from coal.source import Source
from coal.processor import Processor

source = Source()


class Host(object):
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.furnaces = []
        self.furnace_node_map = {}
        self.categories = []
        # get our Nodes
        for node in source.get_nodes(bucket=self.name + '.*'):
            self.nodes.append(node)
        # see which Processors are relevant to us
        for furnace in Processor.host_processors:
            for node in self.nodes:
                if furnace.matches(node):
                    self.furnaces.append(furnace)
                    if furnace not in self.furnace_node_map:
                        self.furnace_node_map[furnace] = []
                    self.furnace_node_map[furnace].append(node)
        self.categories = list(set([furnace.category for furnace in self.furnaces]))

    def categories(self):
        return self.categories

    def get_category(self, category):
        soot = []
        for furnace in self.furnaces:
            if furnace.category == category:
                fuel = []
                for node in self.nodes:
                    if furnace.matches(node):
                        fuel.append(node)
                soot.append(furnace.burn(fuel))
        return soot

