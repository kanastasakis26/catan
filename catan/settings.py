import json

DB_CONFIG = {
    'path': 'sqlite:///experiment.sqlite'
}

EXPERIMENTS = []

def from_config(path):
    with open(path) as f:
        config = json.load(f)

        if 'db_path' in config:
            DB_CONFIG['path'] = "sqlite:///" + config['db_path']

        if 'experiments' in config:
            EXPERIMENTS.extend(config['experiments'])
