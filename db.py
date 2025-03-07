from sqlalchemy import create_engine, Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from db_credentials_info import Credentials

engine = create_engine("postgresql://{}:{}@{}:{}/citricsheep_devtest".format(
    Credentials.User,
    Credentials.Password,
    Credentials.Host,
    Credentials.Port
))

baseDec = declarative_base()

sessionMaker = sessionmaker(bind=engine)

class ElevatorState(baseDec):
    __tablename__ = "states"
    id = Column(Integer, primary_key=True, autoincrement=True)
    elevator_id = Column(Integer)
    current_floor = Column(Integer)
    target_floor = Column(Integer)
    date = Column(DateTime)
    moving = Column(Boolean)
    vacant = Column(Boolean)

class ElevatorDemand(baseDec):
    __tablename__ = "demands"
    id = Column(Integer, primary_key=True, autoincrement=True)
    elevator_id = Column(Integer)
    date = Column(DateTime)
    state_id = Column(Integer, ForeignKey('states.id')) #Reference to the state it when it got this demand
    demanded_floor = Column(Integer)

if __name__ == "__main__":
    baseDec.metadata.create_all(engine)
