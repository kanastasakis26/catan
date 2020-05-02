import json
import networkx as nx 

from catan.experiment.trial import StarPatternTrial
from catan.experiment.tile import Tile, TileNumberGenerator
from catan.experiment.misc import search
from catan.db.db_helper import db_helper


'''
Generate the lattice
Find a way to label the tiles
Assign a number to each tile 
    [2, 12] - one each
    [3,4,5,6,7,8,9,10,11] - two each
Create road settlement pattern 
Roll the dice
Calculate cards produced

What is the average number of resources produced?
Should the board number be randomized with every iteration?
'''
class Experiment:
    def __init__(self, trial_class, n_trials=10, n_rolls=10):
        # Set the number of trials
        self.n_trials = n_trials
        self.n_rolls = n_rolls
        self.trial_class = trial_class

        # Create the board
        self.G = nx.hexagonal_lattice_graph(4,4)

        # Generate tiles
        tiles = dict()
        for node in nx.nodes(self.G):
            # Find the tiles in the lattice. 
            tile_nodes = search(self.G, node)
            tile = Tile(tile_nodes)
            tile_hash = hash(tile)
            if tile_hash not in tiles:
                tiles[tile_hash] = tile
        tiles = dict([(f'Tile-{i}', val) for i, val in enumerate(tiles.values())])

        # Then for each annotate each node with the adjoining tiles
        tile_n_generator = TileNumberGenerator()
        for tile in tiles.values():
            tile.set_n(tile_n_generator.draw())
        
        # Set the tiles
        self.tiles = tiles

        # Save to the db
        tiles_json = json.dumps([t.to_json() for t in tiles.values()])
        db_helper.save_experiment(trial_class.__name__, 'nx.hexagonal_lattice_graph(4,4)', tiles_json)

        # nx.draw(self.G, pos=nx.get_node_attributes(self.G, 'pos'), with_labels=True)
        # plt.show()

    def run_trials(self):
        for n in range(self.n_trials):
            trial = self.trial_class(self.G, self.tiles, self.n_rolls)
            trial.run()

