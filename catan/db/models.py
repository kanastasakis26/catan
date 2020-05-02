from sqlalchemy import Column, Integer, String

from catan.db import Base


class Experiment(Base):
    __tablename__ = 'experiment'

    id = Column(Integer, primary_key=True)
    settlement_pattern = Column(String)
    graph_description = Column(String)
    tiles = Column(String)

    def __repr__(self):
        return f'<Experiment(id={self.id}, graph={self.graph_id} set-pat={self.settlement_pattern})>'


class Trial(Base):
    __tablename__ = 'trial'

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer)
    settlements = Column(String)

    def __repr__(self):
        return f'<Trial(id={self.id}, exp_id={self.experiment_id})>'


class  TrialRoll(Base):
    __tablename__ = 'trial_roll'

    id = Column(Integer, primary_key=True)
    trial_id = Column(Integer)
    roll = Column(Integer)
    resource_count = Column(Integer)

    def __repr__(self):
        return f'<TrialRoll(id={self.id}, trial_id={self.trial_id} roll={self.roll}, res-cnt={self.resource_count})>'




