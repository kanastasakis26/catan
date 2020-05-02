import json
import random
import networkx as nx
from catan.db.db_helper import db_helper
from catan.experiment.misc import roll_dice


class TrialBase:

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
        self._run()
        self.clean_up()

    def _create_settlements(self):
        pass

    def _run(self):
       pass

    def clean_up(self):
        self.G = None
        self.tiles = None
        self.settlements = None


class TrialRunNoRobber:
     def _run(self):
        """
        Override, if needed
        """
        for n in range(self.n_rolls):
            # Roll the dice
            roll = roll_dice()

            tiles = filter(
                lambda t: t.n == roll,
                self.tiles.values()
            )

            resource_count = 0
            for settlement in self.settlements:
                resource_count = resource_count + sum(
                    map(
                        lambda x: 1 if settlement in x.nodes else 0,
                        tiles
                    )
                )
            db_helper.save_trial_roll(roll, resource_count)



class StarPatternTrial(Trial):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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


class RandomTrial(Trial):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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


class PerimeterPatternTrial(Trial):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create_settlements(self):
        tiles = list(self.tiles.values())
        i = random.randint(0, len(tiles) - 1)
        j = random.randint(0, 1)
        self.settlements = tiles[i].nodes[j::2]

