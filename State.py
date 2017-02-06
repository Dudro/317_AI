from World import World
from utils import combinations, permutations_exclude
import copy


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
        Returns the world state.

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
        delivered or not.

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

    def sum_of_package_cost_h(self):
        """
        A heuristic that computes the sum of the cost between each package and
        its destination. This is >0 for all undelivered package, and 0 for all
        delivered packages.

        :rtype: float
        """
        sum_of_package_costs = 0
        for i, pack in enumerate(self._packages):
            if not pack:  # if package is not yet delivered
                sum_of_package_costs += self._world.get_package_cost(i)
        return sum_of_package_costs

    def sum_of_package_cost_scaled_h(self):
        """
        A heuristic that computes the sum of the cost between each package and
        its destination, and then scales down the heuristic by 1 - k/K, where
        k is the number of packages delivered and K is the total number of
        packages. The idea is that, as more packages are delivered, the
        heuristic drops to 0 faster than simply by the computing the sum, and
        this may give search algorithms more of an incentive to drop off a
        package (since a heuristic value closer to 0 implies that we are closer
        to a goal state).

        :rtype: float
        """
        sum_of_package_costs = self.sum_of_package_cost_h()
        num_delivered = self.get_num_delivered()
        reduction_val = 1.0 / float(len(self._packages))
        scalar = 1 - (num_delivered * reduction_val)
        return scalar * sum_of_package_costs


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
    :type state: X, where X is a state type
    :rtype: bool
    """
    for car in range(state.get_world().get_number_of_cars()):
        if state.get_car_loc(car) != state.get_world().get_garage():
            return False
    return state.all_packages_delivered()


def decorating_f(h):
    """
    Returns a function that takes a state, x, of type X, and returns
    f(x) = g(x) + h(x). The given parameter should be the function h.

    :param h: the heuristic function
    :type h: X => float, where X is a state type
    :rtype: X => float, where X is a state type
    """

    def true_f(state):
        return state.get_g() + h(state)

    return true_f


def recreate_paths(state):
    """
    Returns a list of paths, one for each car, that traces the car's path in
    the original map from the initial state (where each car is in the garage)
    to the given state.

    :param state: the state for which to recreate the car paths
    :type state: X, where X is a state type
    :rtype: list(list(int))
    """
    all_paths = []
    world = state.get_world()
    for car_stack in state.get_car_locs():
        if len(car_stack) == 1:  # Car is still at garage
            this_path = [car_stack.pop()]
        else:
            loc = car_stack.pop()
            this_path = []
            while car_stack:  # Means "while car_stack is not empty"
                prev = car_stack.pop()
                if prev != loc:
                    if this_path:  # Means "if this_path is not empty"
                        this_path.pop()  # Remove last item; it's duplicated.
                    this_path.extend(world.get_shortest_path(loc, prev))
                loc = prev
            this_path.reverse()
        all_paths.append(this_path)
    return all_paths


class VanillaState(State):
    """
        A VanillaState simply represents a state in the vanilla state space.
        """

    def __init__(self, world, car_locs, packages, cost_so_far, held):
        """
        :param world: see State constructor
        :param car_locs: see State constructor
        :param packages: see State constructor
        :param cost_so_far: see State constructor
        :param held: a list of indices of the package each car is holding, or
            -1 for any car that is not holding a package
        :type held: list(int)
        """
        super(VanillaState, self).__init__(world, car_locs, packages,
                                           cost_so_far)
        self._held = held

    def __eq__(self, other):
        """
        Two states are considered equal if they have the same number of cars,
        if the *current* location of each car is the same in both states, if
        the same cars are holding packages, if the same packages are being
        held, and if the same packages have been delivered. The path each car
        has taken to reach its current location, and the order in which packages
        were delivered (and which car delivered them) is *not* considered for
        determining state equality.

        :param other: another state
        :type other: VanillaState
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
        other_held = other.get_held()
        for i, held in enumerate(self._held):
            if held != other_held[i]:
                return False
        return True

    def get_cars_in_garage(self):
        """
        Returns a list of car indices for the cars that are in the garage.

        :rtype: list(int)
        """
        return [i for i, car in enumerate(self._car_locs) if car[len(car) - 1]
                == self._world.get_garage()]

    def get_held(self):
        """
        Returns a list of indices of the package each car is holding, or -1
        for any car that is not holding a package.

        :rtype: list(int)
        """
        return self._held

    def get_package_loc(self, k):
        """
        Returns the current location of package 'k'.

        :param k: the index of the package
        :rtype: int
        """
        world = self._world
        if self._packages[k]:  # If package k is delivered.
            return world.get_package_dest(k)
        else:
            for i, held in enumerate(self._held):
                if held == k:  # If car i is holding package k.
                    return self.get_car_loc(i)  # Return car i's location.
            return world.get_package_source(k)  # Since package k is not held.

    def sum_of_estimated_cost_h(self):
        """
        A heuristic that computes the sum of the estimated cost between each
        package and its destination. This is >0 for all undelivered package,
        and 0 for all delivered packages. For undelivered packages, in the
        worst case, the package needs to leave its current location by the
        cheapest outgoing edge. Also, if the package is not adjacent to its
        destination, it needs to enter its destination by the cheapest incoming
        edge to its destination.

        :rtype: float
        """
        cost = 0
        world = self._world
        for i, pack in enumerate(self._packages):
            if not pack:  # If package i is not delivered.
                loc = self.get_package_loc(i)
                cost += world.get_cheapest_edge(loc)
                # Is this package more than one edge away from its destination?
                destination = world.get_package_dest(i)
                if not (loc in world.get_full_map()[destination].keys()):
                    cost += world.get_cheapest_edge(destination)
        return cost

    def sum_of_estimated_cost_scaled_h(self):
        """
        A heuristic that computes the sum of the estimated cost between each
        package and its destination, and then scales down the heuristic by 1/k,
        where k is the number of undelivered packages. The idea is that, as
        more packages are delivered, the heuristic drops to 0 faster than
        simply by the computing the sum, and this may give search algorithms
        more of an incentive to drop off a package (since a heuristic value
        closer to 0 implies that we are closer to a goal state).

        :rtype: float
        """
        base_cost = self.sum_of_estimated_cost_h()
        num_delivered = self.get_num_delivered()
        reduction_val = 1.0 / float(len(self._packages))
        scalar = 1 - (num_delivered * reduction_val)
        return base_cost * scalar


def recursive_neighbour_generator(number_of_cars, i, car_locs, world,
                                  ignore=None):
    if ignore is None:
        ignore = []
    if i == number_of_cars:
        yield []
    elif i in ignore:
        next_car = recursive_neighbour_generator(number_of_cars, i + 1,
                                                 car_locs, world)
        while True:
            result = next(next_car)
            if not result:  # If result is empty.
                yield [car_locs[i][len(car_locs[i]) - 1]]
                break
            yield [car_locs[i][len(car_locs[i]) - 1]] + result
    else:
        adjacency = dict(
            world.get_full_map()[car_locs[i][len(car_locs[i]) - 1]])
        while len(adjacency) != 0:
            next_neighbour = adjacency.popitem()
            next_car = recursive_neighbour_generator(number_of_cars, i + 1,
                                                     car_locs, world)
            while True:

                result = next(next_car)
                if not result:  # If result is empty.
                    yield [next_neighbour[0]]
                    break
                else:
                    yield [next_neighbour[0]] + result
        yield []


def state_transition_vanilla(state):
    successors = []
    world = state.get_world()
    number_of_cars = world.get_number_of_cars()
    # print("INITIAL HELD: " + str(state.get_held()))
    if state.all_packages_delivered():
        for combo in recursive_neighbour_generator(
                number_of_cars, 0, state.get_car_locs(), world,
                ignore=state.get_cars_in_garage()):
            if combo and len(combo) == number_of_cars:
                new_car_locs = [[world.get_garage()]] * number_of_cars
                new_g = state.get_g()
                for n in range(number_of_cars):
                    new_car_locs[n] = copy.deepcopy(state.get_car_path(n))
                for i in range(number_of_cars):
                    if state.get_car_loc(i) != world.get_garage():
                        start = state.get_car_loc(i)
                        end = combo[i]

                        for edge in list(
                                world.get_full_map().edges(data='weight',
                                                           default=1)):
                            if edge[0] == start and edge[1] == end:
                                new_g += edge[2]
                                # print("Added to g " + str(edge[2]) + ", total: " + str(edge[2] + state.get_g()))
                                break
                        new_car_locs[i].append(combo[i])

                new_state = VanillaState(world, new_car_locs,
                                         state.get_packages(),
                                         new_g, state.get_held())
                if new_state != state:
                    successors.append(new_state)

        return successors
    current_packages = state.get_packages()
    for i in range(1, number_of_cars + 1):
        # print("Trying all combinations with all but", i, "cars moving.")
        for cars in combinations(number_of_cars, i):
            # print("Ignore cars: " + str(cars))
            for combo in recursive_neighbour_generator(number_of_cars, 0,
                                                       state.get_car_locs(),
                                                       world, ignore=cars):
                # print("Some Destinations: " + str(combo))
                if combo and len(combo) == number_of_cars:
                    new_car_locs = [[world.get_garage()]] * number_of_cars
                    new_g = state.get_g()
                    for n in range(number_of_cars):
                        new_car_locs[n] = copy.deepcopy(state.get_car_path(n))
                    new_packages = copy.deepcopy(current_packages)
                    new_held = copy.deepcopy(state.get_held())
                    for j in range(number_of_cars):
                        start = state.get_car_loc(j)
                        end = combo[j]
                        # calculate g for car movement in this step
                        for edge in list(
                                world.get_full_map().edges(data='weight',
                                                           default=1)):
                            if edge[0] == start and edge[1] == end:
                                new_g += edge[2]
                                # print("Added to g " + str(edge[2]) + ", total: " + str(edge[2] + state.get_g()))
                                break
                        new_car_locs[j].append(combo[j])
                        # detect if we dropped off a package after moving
                        if new_held[j] != -1:
                            held_package = new_held[j]
                            if world.get_package_dest(held_package) == end:
                                new_packages[held_package] = True
                                new_held[j] = -1
                    # make permutations of picking up packages
                    impossible_pickups = [False] * len(new_packages)
                    possible_count = len(new_packages) + 1
                    # print("possible: " + str(possible_count) + ", new_packages: " + str(new_packages))
                    for k in range(len(new_packages)):
                        if not new_packages[k]:
                            # print("" + str(world.get_package_source(k)) + ", " + str(combo))
                            if not (world.get_package_source(k) in combo):
                                impossible_pickups[k] = True
                                possible_count -= 1
                        else:
                            impossible_pickups[k] = True
                            possible_count -= 1
                    # Impossible_pickups now contains all the packages to
                    # exclude from the permutation.

                    new_state = VanillaState(world, new_car_locs,
                                             new_packages, new_g, new_held)

                    if new_state != state:
                        successors.append(new_state)
                        # print("Appended state with no packages collected")
                    for j in range(1, possible_count):
                        possible_held = copy.deepcopy(new_held)
                        for packs_perm in permutations_exclude(
                                possible_count, j, exclude=impossible_pickups):
                            for pack in packs_perm:
                                # print(packs_perm)
                                for n in range(len(new_car_locs)):
                                    if possible_held[n] == -1 and \
                                                    new_car_locs[n][len(
                                                        new_car_locs[n]) - 1] \
                                                    == world.get_package_source(
                                                pack):
                                        possible_held[n] = pack
                                        break
                                # print("Packs: " + str(possible_held))
                                new_state = VanillaState(world, new_car_locs,
                                                         new_packages, new_g,
                                                         possible_held)
                                # print("Generated successor: ", flush=True)
                                # print(new_state.get_car_locs(), flush=True)
                                # print(new_state.get_packages(), flush=True)

                                if new_state != state:
                                    successors.append(new_state)
                                    # print("Appended state with some cars")
    # print("Wrap-around!")
    # print("Now run it with all the cars moving.")
    for combo in recursive_neighbour_generator(number_of_cars, 0,
                                               state.get_car_locs(), world):

        if combo and len(combo) == number_of_cars:
            new_car_locs = [[world.get_garage()]] * number_of_cars
            new_g = state.get_g()
            for n in range(number_of_cars):
                new_car_locs[n] = copy.deepcopy(state.get_car_path(n))
            new_packages = copy.deepcopy(current_packages)
            new_held = copy.deepcopy(state.get_held())

            for i in range(number_of_cars):
                # print("All Destinations: " + str(combo))
                start = state.get_car_loc(i)
                end = combo[i]
                # calculate g for car movement in this step
                for edge in list(
                        world.get_full_map().edges(data='weight', default=1)):
                    if edge[0] == start and edge[1] == end:
                        new_g += edge[2]
                        # print("Added to g " + str(edge[2]) + ", total: " + str(edge[2] + state.get_g()))
                        break
                new_car_locs[i].append(combo[i])
                # detect if we dropped off a package after moving
                if new_held[i] != -1:
                    held_package = new_held[i]
                    if world.get_package_dest(held_package) == end:
                        new_packages[held_package] = True
                        new_held[i] = -1

            # make permutations of picking up packages
            impossible_pickups = [False] * len(new_packages)
            possible_count = len(new_packages) + 1
            for k in range(len(new_packages)):
                if not new_packages[k]:
                    if not (world.get_package_source(k) in combo):
                        impossible_pickups[k] = True
                        possible_count -= 1
                else:
                    impossible_pickups[k] = True
                    possible_count -= 1
            # impossible_pickups now contains all the packages to exclude
            # from the permutation
            new_state = VanillaState(world, new_car_locs,
                                     new_packages, new_g, new_held)

            if new_state != state:
                successors.append(new_state)
                # print("Appended state with no packages collected")
            for j in range(1, possible_count):
                possible_held = copy.deepcopy(new_held)
                for packs_perm in permutations_exclude(
                        possible_count, j, exclude=impossible_pickups):
                    for pack in packs_perm:
                        # print(packs_perm)
                        for n in range(len(new_car_locs)):
                            if possible_held[n] == -1 and \
                                            new_car_locs[n][len(
                                                new_car_locs[n]) - 1] \
                                            == world.get_package_source(
                                        pack):
                                possible_held[n] = pack
                                # print("PICKED UP!")
                                break
                        # print("Packs: " + str(possible_held))

                        new_state = VanillaState(world, new_car_locs,
                                                 new_packages, new_g,
                                                 possible_held)
                        # print("Generated successor: ", flush=True)
                        # print(new_state.get_car_locs(), flush=True)
                        # print(new_state.get_packages(), flush=True)

                        if new_state != state:
                            successors.append(new_state)
    # print("Appended state with all cars")
    # print("Successors for this node: " + str(len(successors)))
    return successors
