from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_credentials_info import Credentials
import db

engine = create_engine("postgresql://{}:{}@{}:{}/citricsheep_devtest".format(
    Credentials.User,
    Credentials.Password,
    Credentials.Host,
    Credentials.Port
))

sessionMaker = sessionmaker(bind=engine)


class Elevator():
    """ 
    Simple elevator class that demonstrates the behavior that i assume it has and
    and when, according to my toughts, would the date be collected.
    """
    def __init__(self, elevator_id):
        self.e_id = elevator_id
        self.current_floor = None
        # Floor that it's moving towards, if it is moving
        self.target_floor = None
        self.moving = False

        # Irelevant to our data perspective, it would have a usage if wasn't explicit
        # that the elevator is automatically resting if it isn't moving and it's vacant. 
        # Stilla used for the execution of the elevator, that will be abstracted and 
        # simplified in this code as it isn't relevant for the data perspective.
        self.demands = [] 
        
        # I'm assuming that a elevator is considered vacant only if there's 
        # no people inside, even if it has demands left on the queue
        self.vacant = True


    def create_demand(self, floor):
        demanded_at = datetime.now()

        sess = sessionMaker()

        newState = db.NewState(self.e_id, self.current_floor, self.target_floor, demanded_at, self.moving, self.vacant)
        sess.add(newState)
        sess.commit()

        newDemand = db.NewDemand(self.e_id, newState.id, demanded_at, floor)
        sess.add(newDemand)
        sess.commit()

        sess.close()

        # Here would be added the to the demands list, that would be used as a queue
        # In order to the elevator to function properly

    def stop(self, floor, vacant=None):
        """ The elevator stopped at a floor, it could be waiting for someone to leave,
        someone to enter or it could be resting. """

        # The only values that are relevant are:
        date = datetime.now()
        self.moving = False
        self.current_floor = floor
        self.target_floor = None

        # Here the vacancy could be updated, if people leave or enter
        if vacant is not None:
            self.vacant = vacant

        sess = sessionMaker()
        sess.add(db.NewState(self.e_id, self.current_floor, self.target_floor, date, self.moving, self.vacant))
        sess.commit()
        sess.close()


        pass

    def move(self, floor, vacant=None):
        """ The elevator is starting to move towards a floor.
        It could be moving for multiple purposes, but i'm going to abstract,
        again, only the needed information"""
        self.target_floor = floor
        self.moving = True
        date=datetime.now()

        if vacant is not None:
            self.vacant = vacant

        sess = sessionMaker()
        sess.add(db.NewState(self.e_id, self.current_floor, self.target_floor, date, self.moving, self.vacant))
        sess.commit()
        sess.close()

        

    def execution_loop(self):
        """ This is the function that controls the autonomy of the elevatora
        it decides when it calls each function, each floor to go and etcetera."""
        # As this execution will be done manually by the tests, this function 
        # will not be implemented as it isn't specifically relevant for the
        # Data ingestion perspective.
        pass
