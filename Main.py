import State as s
import World as w 
import test_graphs as tg
import graphs as g
import astar

def is_goal(state):
    """
    Determines whether the given state is a goal state.

    :param state: A particular State
    :type state: State
    :rtype: True if this state is a goal state,
        False otherwise.
    """
    return False if False in state.get_packages() else True

def f(state):
    return state.get_g() + state.zero_h()
	
if __name__ == "__main__":
        #tg.test_graphs()
        print("Starting triangle test", flush=True)
        
        n = 1
        k = 2
        m = 3
        map, pairs = g.get_triangle_graph()
		
        world = w.World(n, k, m, map, pairs)
        world.process_map()
        s.world = world
        print((s.world == None), flush=True)
        cars = [[0] * n]
        packages = [False] * k
		
        initial = s.State( cars, packages, 0)
		
        for solution in astar.astar(initial, is_goal, s.state_transition, f):
            print(str(solution.get_g()))
        print("Done triangle", flush=True)
        
        print("Starting OGG test")
        
        n = 1
        k = 3
        m = 9
        map, pairs = g.get_og_graph()
		
        world = w.World(n, k, m, map, pairs)
        world.process_map()
        s.world = world
        cars = [[0] * n]
        packages = [False] * k
		
        initial = s.State( cars, packages, 0)
		
        for solution in astar.astar(initial, is_goal, s.state_transition, f):
            print(str(solution.get_g()))
        print("Done")
    
