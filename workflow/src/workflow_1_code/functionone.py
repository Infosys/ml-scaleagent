from .functiontwo import functiontwo

def functionone(events):
    # functionone, functiontwo and functionthree are examples/teamplates.
    # In developement environment, these functions will contain the actual inference logic.
    # The function names inside the workflow_1_code can be changed to represnt the real world model use case.
    return functiontwo(events)
