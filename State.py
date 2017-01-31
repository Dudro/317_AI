import copy
from World import World
from utils import *


class State:
    """
    A State simply represents a state in the state space.
    """

    def __init__(self, world, car_locs, packages, cost_so_far):
        """
        :param world: the world state that is unchanging but still part of
            every state
        :type world: World
        :param car_locs: a list of stacks keeping track of each car's
            current location and path so far
        :type car_locs: list(list(int))
        :param packages: a list of booleans showing whether each package
            has been delivered or not
        :type packages: list(bool)
        :param cost_so_far: the total cost so far from the start state this
            state. This is later referred to as 'g'.
        :type cost_so_far: float
        """
        self._world = world
        self._car_locs = car_locs
        self._packages = packages
        self._g = cost_so_far

    def __eq__(self, other):
        """
        Two states are considered equal if they have the same number of cars,
        if the *current* location of each car is the same in both states, and
        if the same packages have been delivered. The path each car has taken
        to reach its current location, and the order in which packages were
        delivered (and which car delivered them) is *not* considered for
        determining state equality.
        :param other: another state
        :type other: State
        :rtype: bool
        """
        other_cars = other.get_car_locs()
        for i, car in enumerate(self._car_locs):
            if car[len(car) - 1] != other_cars[i][len(other_cars[i]) - 1]:
                return False
        other_packs = other.get_packages()
        for i, pack in enumerate(self._packages):
            if pack != other_packs[i]:
                return False
        return True

    def get_world(self):
        """
        Returns the world state
        :rtype: World
        """
        return self._world

    def get_g(self):
        """
        Returns g(x), the cost so far.

        In A*, states are examined in order of least f-value, where, for any
        state x, f(x) = g(x) + h(x), where g(x) is the total cost so far from
        the initial state to state x, and h(x) is the heuristic estimating the
        remaining cost still to be incurred between x and a goal state.
        :rtype: float
        """
        return self._g

    def get_car_locs(self):
        """
        For each car, returns a stack recording the car's path over time.
        :rtype: list(list(int))
        """
        return self._car_locs

    def get_packages(self):
        """
        Returns a list of booleans showing whether each package has been
            delivered or not
        :rtype: list(bool)
        """
        return self._packages

    def get_car_path(self, n):
        """
        Returns a stack recording the n'th car's path over time.
        :param n: the index of the car
        :rtype: list(int)
        """
        return self._car_locs[n]

    def get_car_loc(self, n):
        """
        Returns the current location of the n'th car.
        :param n: the index of the car
        :rtype: int
        """
        return self._car_locs[n][len(self._car_locs[n]) - 1]

    def get_num_delivered(self):
        """
        Returns the number of packages that have already been delivered.
        :rtype: int
        """
        return self._packages.count(True)

    def get_num_undelivered(self):
        """
        Returns the number of packages that still need to be delivered.
        :rtype: int
        """
        return self._packages.count(False)

    def all_packages_delivered(self):
        """
        Returns whether all packages have been delivered or not.
        :rtype: bool
        """
        return self.get_num_undelivered() == 0

    # ===== Heuristics ===== #

    def zero_h(self):
        """
        The 0 heuristic. That is, h(x) = 0 for all states x.
        :rtype: int
        """
        return 0

    def undelivered_h(self):
        """
        A heuristic that simply counts the number of undelivered packages.
        :rtype: int
        """
        return self.get_num_undelivered()

    def sum_of_package_distance_h(self):
        """
        A heuristic that computes the sum of the distance between each package
        and its destination. This is >0 for all undelivered package, and 0 for
        all delivered packages.
        :rtype: float
        """
        sum_of_package_distances = 0
        for i, pack in enumerate(self._packages):
            if not pack:  # if package is not yet delivered
                sum_of_package_distances += self._world.get_package_cost(i)
        return sum_of_package_distances

    def sum_of_package_distance_scaled_h(self):
        """
        A heuristic that computes the sum of the distance between each package
        and its destination, and then scales down the heuristic by 1 - k/K,
        where k is the number of packages delivered and K is the total number
        of packages. The idea is that, as more packages are delivered, the
        heuristic drops to 0 faster than simply by the computing the sum, and
        this may give search algorithms more of an incentive to drop off a
        package (since a heuristic value closer to 0 implies that we are closer
        to a goal state).
        :rtype: float
        """
        sum_of_package_distances = self.sum_of_package_distance_h()
        num_delivered = self.get_num_delivered()
        reduction_val = 1.0 / float(len(self._packages))
        scalar = 1 - (num_delivered * reduction_val)
        return scalar * sum_of_package_distances


def state_transition(state):
    """
    Returns a list of all possible successors of the given state.

    The successors are as follows:
    - if the given state has all packages delivered, then the only successor
    state has all the cars back at the garage;
    - otherwise, for each possible combination of cars of each size (from a
    single car to all the cars), for each possible permutations (of the correct
    size) of assignments of the undelivered packages to the chosen cars, we
    create a successor state wherein the chosen cars have moved to their
    assigned package's source (if needed), and then moved their assigned
    package from its source to its destination.
    :param state: the state for which the successors should be found
    :rtype: list(State)
    """
    successors = []
    world = state.get_world()
    number_of_cars = world.get_number_of_cars()
    if state.all_packages_delivered():
        new_car_locs = [[world.get_garage()]] * number_of_cars
        for n in range(number_of_cars):
            new_car_locs[n] = copy.deepcopy(state.get_car_path(n))
        new_packages = copy.deepcopy(state.get_packages())
        new_g = state.get_g()
        for car in range(number_of_cars):
            car_stack = new_car_locs[car]
            if car_stack[len(car_stack) - 1] != world.get_garage():
                new_g += world.get_edge_cost(car_stack[len(car_stack) - 1],
                                             world.get_garage())
                car_stack.append(world.get_garage())
        new_state = State(world, new_car_locs, new_packages, new_g)
        successors.append(new_state)
        return successors
    for i in range(1, number_of_cars + 1):
        # print("Trying all combinations with just", i, "cars moving.")
        for cars in combinations(number_of_cars, i):
            # print("Trying combination:", cars)
            # print("Trying all permutations of", i, "package assignments.")
            for packs_perm in permutations_exclude(
                    len(state.get_packages()), i, state.get_packages()):
                # print("Trying permutation:", packs_perm)
                car_with_pack = [-1] * number_of_cars
                new_car_locs = [[world.get_garage()]] * number_of_cars
                for n in range(number_of_cars):
                    new_car_locs[n] = copy.deepcopy(state.get_car_path(n))
                new_packages = copy.deepcopy(state.get_packages())
                new_g = state.get_g()

                for j in range(0, i):
                    car_with_pack[cars[j]] = packs_perm[j]
                    # print("Car with pack: " + str(car_with_pack), flush=True)
                    # print("Cars: " + str(cars), flush=True)
                    # print("Packs Perm: " + str(packs_perm), flush=True)
                    # update the values of the list state.get_car_locs()
                    # for the new state
                    new_car_locs[cars[j]].append(
                        world.get_package_source(car_with_pack[cars[j]]))
                    new_car_locs[cars[j]].append(
                        world.get_package_dest(car_with_pack[cars[j]]))
                    # update the values of the list state.get_packages()
                    # for the new state
                    if car_with_pack[cars[j]] != -1:
                        new_packages[car_with_pack[cars[j]]] = True
                        new_g += world.get_edge_cost(
                            state.get_car_loc(cars[j]),
                            world.get_package_source(packs_perm[j]))
                        new_g += world.get_package_cost(packs_perm[j])
                # new_state is added to list of successors
                # print("Resulting total cost so far:", new_g)

                new_state = State(world, new_car_locs, new_packages, new_g)
                # print("Generated successor: ", flush=True)
                # print(new_state.get_car_locs(), flush=True)
                # print(new_state.get_packages(), flush=True)
                successors.append(new_state)
    return successors


def is_goal(state):
    """
    Returns whether or not the given state is a goal state. A goal state has
    every package delivered and every car back at the garage.
    :param state: the state to check
    :rtype: bool
    """
    for car in range(state.get_world().get_number_of_cars()):
        if state.get_car_loc(car) != state.get_world().get_garage():
            return False
    return state.all_packages_delivered()
