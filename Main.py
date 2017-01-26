import State as s
import World as w 
import test_graphs as tg

def is_goal(state):
    """
    Determines whether the given state is a goal state.

    :param state: A particular State
    :type state: State
    :rtype: True if this state is a goal state,
        False otherwise.
    """
    for p in state.get_packages():
        if p is False:
            return False
    return True

if __name__ == "__main__":
        tg.test_graphs()

    

    
