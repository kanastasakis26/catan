from catan.experiment.experiment import Experiment
from catan.experiment.trial import RandomTrial, StarPatternTrial, PerimeterPatternTrial

def run_star_pattern_experiment(n_trials, n_rolls):
    experiment = Experiment(StarPatternTrial, n_trials=n_trials, n_rolls=n_rolls)
    experiment.run_trials()


def run_random_experiment(n_trials, n_rolls):
    experiment = Experiment(RandomTrial, n_trials=n_trials, n_rolls=n_rolls)
    experiment.run_trials()


def run_perimeter_experiment(n_trials, n_rolls):
    experiment = Experiment(PerimeterPatternTrial, n_trials=n_trials, n_rolls=n_rolls)
    experiment.run_trials()


def run_experiment(settlement_pattern, n_trials, n_rolls):
    if settlement_pattern == 'star':
        run_star_pattern_experiment(n_trials, n_rolls)
    elif settlement_pattern == 'random':
        run_random_experiment(n_trials, n_rolls)
    elif settlement_pattern == 'perimeter':
        run_perimeter_experiment(n_trials, n_rolls)
