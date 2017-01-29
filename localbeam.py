def local_beam_search(k,state,is_goal) 
    """k: # of states are being considered
       state: a particular state
       is_goal: a function to check whether or not goal is achieved
       retun: a goal_state        
    """
    #if is_goal(state) is false then
        #apply state_transition function to state which would return a list of successor as candidate[]
        #generate a priority queue called potential[]
        #find the minimum cost from all possibilities return by state_transition
        #state with minimum cost has the highest priority in the queue; append this to potential[];pop it out of candidate[]
        #choose (k-1) states from candidate and append them to potential[]
        #apply local_beam_search on each of the state in potential[]
   #if is_goal(state) is true then return state as a goal_state           
