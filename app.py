from datetime import datetime


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
        self.vacant = True

        # Irelevant to our data perspective, it would have a usage if wasn't explicit
        # that the elevator is automatically resting if it isn't moving and it's vacant. 
        # Stilla used for the execution of the elevator, that will be abstracted and 
        # simplified in this code as it isn't relevant for the data perspective.
        self.demands = [] 

    def create_demand(self, floor):
        demanded_at = datetime.now()

    def stop():
        """ The elevator stopped at a floor, it could be waiting for someone to leave,
        someone to enter or it could be resting. """
        pass

    def move():
        """ The elevator is starting to move towards a floor."""

    def execution_loop(self):
        """ This is the function that controls the autonomy of the elevatora
        it decides when it calls each function, each floor to go and etcetera."""
        # As this execution will be done manually by the tests, this function 
        # will not be implemented as it isn't specifically relevant for the
        # Data ingestion perspective.
        pass
