import json
import random
import networkx as nx
from catan.db.db_helper import db_helper
from catan.experiment.misc import roll_dice, die_roll_prob


class Trial:

    def __init__(self, G, tiles, n_rolls=10):
        self.G = G
        self.tiles = tiles
        self.n_rolls = n_rolls
        self.settlements = None

    def run(self):
        # Create settlements
        self._create_settlements()

        # Check they exist
        if not self.settlements:
            raise Exception("Must have settlements")
        
        # Save the trial
        db_helper.save_trial(json.dumps(list(self.settlements)))

        # Run the trial
        results = self._run()
        db_helper.save_trial_roll_bulk(results)
        
        self.clean_up()

    def _create_settlements(self):
        raise Exception('Must implement _create_settlements.')

    def _run(self):
       raise Exception('Must implement _run.')

    def clean_up(self):
        self.G = None
        self.tiles = None
        self.settlements = None


class TrialRunNoRobber:
    def _run(self):
        results = []
        for n in range(self.n_rolls):
            # Roll the dice
            roll = roll_dice()

            # Filter then convert to a list
            tiles = filter(
                lambda t: t.n == roll,
                self.tiles.values()
            )
            # Convert filter object to list for multiple traversals
            tiles = list(tiles)

            resource_count = 0
            for settlement in self.settlements:
                resource_count = resource_count + sum(
                    map(
                        lambda x: 1 if settlement in x.nodes else 0,
                        tiles
                    )
                )
            results.append((roll, resource_count))
        
        return results

class TrialRunWithRobber:

    def _place_robber(self):
        tile_name = None

        # Roll the dice
        # Another option is to use a distribution
        # of having rolled a seven and a distribution 
        # of having been targeted
        previous_roll = roll_dice()

        settlements_as_set = set(self.settlements)
        selected_tile = None
        score = -1
        if previous_roll == 7 or True:
            # Place the robber on the tile that
            # removes greatest gains from gameplay
            # Use expectation of resource count as a score
            # Probability of rolling N * Number of settlements on a tile

            tiles = self.tiles.items()
            for key, tile in tiles:
                p = die_roll_prob(tile.n)
                s = len(settlements_as_set.intersection(set(tile.nodes)))

                _score = p * s
                if _score > score:
                    score = _score
                    tile_name = key

        return tile_name

    def _run(self):
        results = []
        for n in range(self.n_rolls):
            robber_tile = self._place_robber()

            roll = roll_dice()
            # Filter out the robber tile
            tiles = map(
                lambda x: x[1],
                filter(
                    lambda kv: kv[1].n == roll and kv[0] != robber_tile,
                    self.tiles.items()
                )
            )
            # Convert filter object to list for multiple traversals
            tiles = list(tiles)

            resource_count = 0
            for settlement in self.settlements:
                resource_count = resource_count + sum(
                    map(
                        lambda x: 1 if settlement in x.nodes else 0,
                        tiles
                    )
                )
            
            results.append((roll, resource_count))

        return results

# ============================================================
#                     No Robber
# ============================================================


class StarPatternTrial(TrialRunNoRobber, Trial):

    def _create_settlements(self):
        settlements = None
        nodes = list(nx.nodes(self.G))
        n_nodes = len(nodes)

        while settlements is None:
            i = random.randrange(0, n_nodes)
            cluster_center = nodes[i]
            neighbors = list(nx.neighbors(self.G, cluster_center))
            if len(neighbors) == 3:
                settlements = set(neighbors)
        
        self.settlements = settlements


class RandomTrial(TrialRunNoRobber, Trial):

    def _create_settlements(self):
        settlements = set()
        nodes = list(nx.nodes(self.G))
        n_nodes = len(nodes)

        while len(settlements) < 3:
            i = random.randrange(0, n_nodes)
            node = nodes[i]
            if node not in settlements:
                settlements.add(node)
        
        self.settlements = settlements


class PerimeterPatternTrial(TrialRunNoRobber, Trial):

    def _create_settlements(self):
        tiles = list(self.tiles.values())
        i = random.randint(0, len(tiles) - 1)
        j = random.randint(0, 1)
        self.settlements = tiles[i].nodes[j::2]


# ============================================================
#                    With Robber
# ============================================================


class StarPatternTrialWithRobber(TrialRunWithRobber, Trial):

    def _create_settlements(self):
        settlements = None
        nodes = list(nx.nodes(self.G))
        n_nodes = len(nodes)

        while settlements is None:
            i = random.randrange(0, n_nodes)
            cluster_center = nodes[i]
            neighbors = list(nx.neighbors(self.G, cluster_center))
            if len(neighbors) == 3:
                settlements = set(neighbors)
        
        self.settlements = settlements


class RandomTrialWithRobber(TrialRunWithRobber, Trial):

    def _create_settlements(self):
        settlements = set()
        nodes = list(nx.nodes(self.G))
        n_nodes = len(nodes)

        while len(settlements) < 3:
            i = random.randrange(0, n_nodes)
            node = nodes[i]
            if node not in settlements:
                settlements.add(node)
        
        self.settlements = settlements


class PerimeterPatternTrialWithRobber(TrialRunWithRobber, Trial):

    def _create_settlements(self):
        tiles = list(self.tiles.values())
        i = random.randint(0, len(tiles) - 1)
        j = random.randint(0, 1)
        self.settlements = tiles[i].nodes[j::2]

