from catan.experiment.experiment import Experiment
from catan.experiment.trial import (
    RandomTrial, 
    RandomTrialWithRobber,
    StarPatternTrial, 
    StarPatternTrialWithRobber,
    PerimeterPatternTrial,
    PerimeterPatternTrialWithRobber,
)

def run_star_pattern_experiment(n_trials, n_rolls, with_robber=False):
    trial_class = StarPatternTrialWithRobber if with_robber else StarPatternTrial
    experiment = Experiment(trial_class, n_trials=n_trials, n_rolls=n_rolls)
    experiment.run_trials()


def run_random_experiment(n_trials, n_rolls, with_robber=False):
    trial_class = RandomTrialWithRobber if with_robber else RandomTrial
    experiment = Experiment(trial_class, n_trials=n_trials, n_rolls=n_rolls)
    experiment.run_trials()


def run_perimeter_experiment(n_trials, n_rolls, with_robber=False):
    trial_class = PerimeterPatternTrialWithRobber if with_robber else PerimeterPatternTrial
    experiment = Experiment(trial_class, n_trials=n_trials, n_rolls=n_rolls)
    experiment.run_trials()


def run_experiment(settlement_pattern, n_trials, n_rolls):
    if settlement_pattern == 'star':
        run_star_pattern_experiment(n_trials, n_rolls)
    elif settlement_pattern == 'star_robber':
        run_star_pattern_experiment(n_trials, n_rolls, True)
    elif settlement_pattern == 'random':
        run_random_experiment(n_trials, n_rolls)
    elif settlement_pattern == 'random_robber':
        run_random_experiment(n_trials, n_rolls, True)
    elif settlement_pattern == 'perimeter':
        run_perimeter_experiment(n_trials, n_rolls)
    elif settlement_pattern == 'perimeter_robber':
        run_perimeter_experiment(n_trials, n_rolls, True)
