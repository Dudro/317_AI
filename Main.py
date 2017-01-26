import State as s
import World as w 
import test_graphs as tg

def is_goal(state):
    """
    :param state: A particular State
    :type state: State
    :rtype: True if this state is a goal state,
        False otherwise.
    """
    return False if False in state.get_packages() else True

if __name__ == "__main__":
        tg.test_graphs()

    

    
