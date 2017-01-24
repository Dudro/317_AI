import World as world_state
class State:

    def __init__(self, carLocs, packages, costSoFar):
        """
        :param carLocs: a list of stacks keeping track of each car's
            current location and path so far
        :type carLocs: list(list(int))
        :param packages: a list of booleans showing whether each package
            has been delivered or not
        :type pacakages: list(bool)
        :param costSoFar: the total cost so far from the start state this
            state. This is later referred to as 'g'.
        :type costSoFar: float
        """
        self._carLocs = carLocs
        self._packages = packages
        self._g = costSoFar
        self._h = 0

    def get_g(self):
        return self._g

    def get_h(self):
        return self._h

    def set_h(self, new):
        self._h = new

    def get_number_of_cars(self):
	return len(self._carLocs)

    def get_carLocs(self):
        return self._carLocs

    def get_packages(self):
        return self._packages

    def get_car_path(self, n):
        if n >= len(self._carLocs):
            return None
        return self._carLocs[n]

    def get_car_loc(self, n):
        return self.get_car_path(n)[len(self.get_car_path(n))-1]

    def get_package_status(self, k):
        if k >= len(self._packages):
            return None
        return self._packages[k]

    def get_num_delivered(self):
        return self._packages.count(True)
   
    def get_num_undelivered(self):
	return self._packages.count(False)

    def get_undelivered_packages(self):
	undelivered=[]
	for x in range(0,len(_packages)):
		if not _packages[x]:
			undelivered.append(x)
			return undelivered


# this function is in between of completion, Needs work on it. Need to work on calculating the sum of path cost.
def stateTransition(state):
    successors = []
    numberOfCars = state.get_number_of_cars();
    unDelivered = state.get_num_undelivered();
    for i in range(0,numberOfCars):
	for cars in combinations(numberOfCars,i):
		for packsPerm in permutations(state.get_undelivered_packages(),i):
			carWithPack = [-1] * numberOfCars	
			#deep copy this, or shallow?
			newCarLocs = copy.deepcopy(state.get_carLocs())
			newPackages = copy.deepcopy(state.get_packages())
			new_g = state.get_g()
			for j in range(0,i):
				carWithPack[cars[j]]=packsPerm[j]
				#update the values of the list state.get_carLocs() for the new state
				newCarLocs[cars[j]] = world_state.get_package_dest(carWithPack[cars[j]])				
				#update the values of the list state.get_packages() for the new state
				if carWithPack[j] != -1:
					newPackages[carWithPack[j]]=True

				new_g += world_state.get_path_cost(state.get_carLocs()[cars[j]], world_state.get_package_source(packsPerm[j]))
				new_g += world_state.get_path_cost(state.get_carLocs()[cars[j]], world_state.get_package_dest(packsPerm[j]))
			#new_state is assigned to updated state of carLocs and packages	
	
			new_state = State(newCarLocs, newPackages, new_g)

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
