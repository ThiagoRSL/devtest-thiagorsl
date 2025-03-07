from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db_credentials_info import Credentials
import db
import pandas as pd

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
        
        # Elevator Id is defined because you can have multiple elevators information
        # in the same building, and this information could be useful for apply a correction
        # on prediction for some scenarious. Such as the maintenance of one elevator on a floor
        # that has two elevators.
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


    def create_demand(self, floor, demanded_at = datetime.now()):

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

    def stop(self, floor, vacant=None, date=datetime.now()):
        """ The elevator stopped at a floor, it could be waiting for someone to leave,
        someone to enter or it could be resting. """

        # The only values that are relevant are:
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

    def move(self, floor, vacant=None, date=datetime.now()):
        """ The elevator is starting to move towards a floor.
        It could be moving for multiple purposes, but i'm going to abstract,
        again, only the needed information"""
        self.target_floor = floor
        self.moving = True
        

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


def simple_test(elevator, sd):
    elevator.create_demand(10, demanded_at=sd) #10th floor demand
    elevator.move(10, date=sd)       #stopped at 10th floor
    sd += timedelta(seconds=30)    #30 seconds after, a new demand
    elevator.create_demand(5, demanded_at=sd)  #5th floor demand
    sd += timedelta(seconds=30)    #30 seconds after, it arrives at 10th floor
    elevator.stop(10, date=sd)       #stopped at 10th floor
    elevator.move(5, date=sd)       #stopped at 10th floor
    sd += timedelta(seconds=40)    #40 seconds after
    elevator.stop(5, date=sd)       #arrives at 5th floor

    return sd
    
def print_data():
    sess = sessionMaker()
    print("\nAll Elevator Demands:")
    for row in sess.execute(text("Select * from demands")):
        print(row)

    print("\nAll Elevator States:")
    for row in sess.execute(text("Select * from states")):
        print(row)
    sess.close()
    

def extract_data():    
    df_states = pd.read_sql("SELECT * FROM states", engine)

    # If the elevator is stopped, target floor became the current_floor
    df_states.loc[df_states["target_floor"].isna(), "target_floor"] = df_states["current_floor"]
    df_states["resting"] = df_states["vacant"] & ~df_states["moving"]
    df_states["unixtime"] = df_states["date"].astype(int) / 10**9

    df_demands = pd.read_sql("SELECT * FROM demands", engine)
    df_demands["unixtime"] = df_demands["date"].astype(int) / 10**9
    df_states.to_csv("elevatorStatesData.csv", index=False)
    df_demands.to_csv("elevatorDemandsData.csv", index=False)

    df_demands_join_states = pd.merge(df_demands, df_states, how="inner", left_on="state_id", right_on="id")
    df_demands_join_states.drop(['id_x', 'id_y', 'state_id', 'elevator_id_y', 'unixtime_y', 'date_y', 'date_x'], axis=1, inplace=True)
    df_demands_join_states.rename(columns={'elevator_id_x': 'elevator_id', 'unixtime_x': 'unixtime',}, inplace=True)

    #print(df_demands_join_states.columns)

    # Save data into csvs
    df_demands_join_states.to_csv("elevatorDemandsJoinStatesData.csv", index=False)


if __name__ == "__main__":
    sess = sessionMaker()

    #Setting up
    elevator = Elevator(1)
    elevator.current_floor = 0

    #starting date of test (simulation)
    sd = datetime(2024,10,1,12,0)
    print("Executing tests...")
    sd = simple_test(elevator, sd)
    print_data()

    # Extract data to csv to train models
    extract_data()


    
