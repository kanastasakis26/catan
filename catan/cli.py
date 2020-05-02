import click
import catan.settings as settings

from catan.analyze import (
    load_data, 
    describe_settlement_pattern,
    test_settlement_pattern_difference
)

import numpy as np

@click.group()
def cli():
    print('Welcome!')


@cli.command()
@click.argument('config_path', required=True, type=click.Path(exists=True))
def experiment(config_path):
    print(f'Loading config from {config_path}')
    settings.from_config(config_path)

    print('Start experiments')
    from catan.experiment import run_experiment

    exp_configs = settings.EXPERIMENTS
    for i, exp_config in enumerate(exp_configs):
        settlement_pattern = exp_config['settlement_pattern']
        n_trials = exp_config['trials']
        n_rolls = exp_config['rolls']

        print(f'Running experiment {i}; settlement_pattern={settlement_pattern}, n_trials={n_trials}, n_rolls={n_rolls}')
        run_experiment(settlement_pattern, n_trials, n_rolls)


@cli.command()
@click.argument('config_path', required=True, type=click.Path(exists=True))
def analyze(config_path):
    print(f'Loading config from {config_path}')
    print('\n')
    settings.from_config(config_path)
    
    df = load_data()

    print(describe_settlement_pattern(df))
    print('\n')
    print(test_settlement_pattern_difference(df))
    print('\n')