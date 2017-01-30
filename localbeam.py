from queue import PriorityQueue
from State import *
import sys
def local_beam_search(state,is_goal,trans_op,f,k):
    """
      :param k: a number of states are being considered
      :type k: Integer
      :param state: a current state
      :type state: State which is defined by car_locs[],packages[],cost_so_far
      :return: goal_state
      :type: State
      :param f: a total cost - compute f(state)= g(state) + h(state)
    #if is_goal(state) is false       
        #apply state_transition function to state which would return a list of successor as candidate[]
        #generate a priority queue called potential[]
        #find the minimum cost from all possibilities return by state_transition
        #state with minimum cost has the highest priority in the queue; append this to potential[];pop it out of candidate[]
        #choose (k-1) states from candidate and append them to potential[]
        #apply local_beam_search on each of the state in potential[]
   #if is_goal(state) is true then return state as a goal_state
   """
    if is_goal(state):
        goal_state = state
        yield goal_state,1
    else:
        #may add a counter here to count how many nodes that we have explored

        potentialTemp = PriorityQueue()
        potential = []
        candidate = trans_op(state)
        cost = []
        min_cost = sys.maxsize
        min_cost_mem = None
        for mem in candidate:
            mem_cost = f(mem)
            # question : Should we check for duplicates or not
            if not potentialTemp.empty():
                if mem_cost not in potentialTemp.queue[0]:
                    potentialTemp.put((mem_cost,mem))
            else:
                potentialTemp.put((mem_cost, mem))
            if k >= len(potentialTemp.queue):
                potential = potentialTemp.queue
            else:
                potential = potentialTemp.queue[0:k]
        # for mem in candidate:
        #     if mem.get_g() == min(cost) and potential.empty():
        #         potential.put(mem)
        #         state_w_min = mem
        #     elif mem state_w_min

        for mem in potential:
            for sol,exp in local_beam_search(mem[1],is_goal,trans_op,f,k):
                yield sol,exp+1
          
        
            
