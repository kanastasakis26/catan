import random
import json

class TileNumberGenerator:
    def __init__(self):
        pop = [2,12] + [3,4,5,6,7,8,9,10,11] * 2
        k = len(pop)
        self.samples = random.sample(pop, k)

    def draw(self):
        return self.samples.pop()


class Tile:
    def __init__(self, nodes):
        self.nodes = nodes  # A list of the nodes in sequence.
        self.n = -1
    
    def __eq__(self, tile):
        return set(self.nodes) == set(tile.nodes)

    def __hash__(self):
        return hash(frozenset(self.nodes))

    def __repr__(self):
        return f'[Tile: {self.nodes}'

    def set_n(self, n):
        self.n = n

    def to_json(self):
        return json.dumps({"nodes": self.nodes, "n": self.n})
    
    # TODO: Write method to convert json to a class instance.


