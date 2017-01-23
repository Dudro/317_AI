class State:

    def __init__ (self, carLocs, packages, costSoFar):
        """
        :param carLocs:
        :type carLocs: list(list(int))
        """
        self._carLocs = carLoc
        self._packages = packages
        self._g = costSoFar
        self._h = 0

    def get_g(self):
        return self._g

    def get_h(self):
        return self._h

    def set_h(self, new):
        self._h = new

    def get_carLocs(self):
        return self._carLocs

    def get_packages(self):
        return self._packages

    def get_car_path(self, n):
        if n >= len(self._carLocs):
            return None
        return self._carLocs[n]

    def get_car_loc(self, n):
        if n >= len(self._carLocs):
            return None
        return self._carLocs[n][len(self._carLocs[n])-1]

    def get_package_status(self, k):
        if k >= len(self._packages):
            return None
        return self._packages[k]

    def get_num_delivered(self):
        sum = 0
        for i in range(len(self._packages)):
            if self._packages[i]:
    		sum += 1
        return sum


def stateTransition(state):
    successors = []
    #go get the world data from somewhere
    #for i in range(1, len(state.get_packages()) - state.get_num_delivered() + 1):
        #for each  combination of N pick i
            #for each permutation of i packages
                #calculate the sum of path costs for this permutation
                #g = state.get_g() + path_cost_sum
                #update the values of the list state.get_carLocs() for the new state
                #update the values of the list state.get_packages() for the new state
                #new_state = State(newLocs, newPackages, g)
    
                #calculate new_state's h() with the problem's chosen heuristic                

                #compare new_state with fringe
                #if it's not a duplicate or if it's a cheaper duplicate
                    #successors.append(new_state)
    return successors
