import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create the database directory
DATABASE_DIR = os.path.join(BASE_DIR, 'databases')
if not os.path.exists(DATABASE_DIR):
    os.mkdir(DATABASE_DIR)

# Create the analysis output directory
REPORT_DIR = os.path.join(BASE_DIR, 'reports')
if not os.path.exists(REPORT_DIR):
    os.mkdir(REPORT_DIR)

DB_CONFIG = {
    'name': '',
    'path': 'sqlite:///experiment.sqlite'
}

EXPERIMENTS = []

def from_config(path):
    with open(path) as f:
        config = json.load(f)

        if 'db_name' in config:
            DB_CONFIG['name'] = config['db_name'].strip()
            DB_CONFIG['path'] = f"sqlite:///{os.path.join(DATABASE_DIR, config['db_name'].strip())}"

        if 'experiments' in config:
            EXPERIMENTS.extend(config['experiments'])
