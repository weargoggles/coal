from coal.hole import Hole
import coal.furnace

furnaces = coal.furnace.get_installed_furnaces()

class Host(object):
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.furnaces = []
        self.categories = []
        # get our Nodes
        h = Hole()
        for node in h.get_coal(branch=self.name+'.*'):
            self.nodes.append(node)
        # see which Furnaces are relevant to us
        for furnace in furnaces:
            for node in self.nodes:
                if furnace.matches(node):
                    self.furnaces.append(furnace)
                    break
        self.categories = list(set([furnace.category for furnace in self.furnaces]))
    
    def categories(self):
        return self.categories
    
    def get_category(self, category):
        soot = []
        for furnace in self.furnaces:
            if furnace.category = category:
                fuel = []
                for node in self.nodes:
                    if furnace.matches(node):
                        fuel.append(node)
                soot.append(furnace.burn(fuel))
        return soot

