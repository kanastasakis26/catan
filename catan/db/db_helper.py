from catan.db import Session
from catan.db.models import (
    Experiment,
    TrialRoll,
    Trial
)

class DBHelper:

    def __init__(self):
        self.experiment = None
        self.trial = None
        self.session = Session()

    def save_experiment(self, settlement_pattern, graph_description, tiles):
        """
        settlement_pattern: Name of the settlement pattern
        graph_description: Graph function and arguments
        tiles: Json of the tiles
        """
        experiment = Experiment(
            settlement_pattern=settlement_pattern, 
            graph_description=graph_description,
            tiles=tiles)

        self.session.add(experiment)
        self.session.commit()

        self.experiment = experiment

    def save_trial(self, settlements):
        """
        settlements: Json of the nodes that have settlements
        """
        trial = Trial(experiment_id=self.experiment.id, settlements=settlements)

        self.session.add(trial)
        self.session.commit()

        self.trial = trial

    def save_trial_roll_bulk(self, result_list):
        """
        result_list: List of tuples. [(roll, resource_count), ... ]
            roll: the sum of the faces from rolling to 6 sided dice
            resource_count: the number of resources earned
        """
        trial_rolls = [TrialRoll(trial_id=self.trial.id, roll=x[0], resource_count=x[1]) for x in result_list]

        self.session.bulk_save_objects(trial_rolls)
        self.session.commit()


db_helper = DBHelper()
