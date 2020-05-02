from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import catan.settings as settings

engine = create_engine(settings.DB_CONFIG['path'])

# Session creator for db interactions
Session = sessionmaker(bind=engine)

# Base class for models
Base = declarative_base()

# Create the tables if they do not exist
# Should be run after all models are defined
from catan.db.models import (
    Experiment,
    Trial,
    TrialRoll
)
Base.metadata.create_all(engine)