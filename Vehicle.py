class Vehicle:
    """
    A Vehicle is the entity moving around the world space graph.
    It picks up and delivers packages.  It always starts and ends 
    its path in the location initially provided to it, assumed to be
    the 'garage.'
    """
    def __init__(self, new_id, loc):
        """
        :param new_id: The unique id of the new vehicle.
        :type new_id: int
        :param loc: The current location of the vehicle. 
        :type loc: int
        """
        
        self._id = new_id
        self._loc = loc
        """ _pkg (int):
        The package the vehicle is currently carrying.
        If it is not carrying a package, _pkg is None. """
        self._pkg = None
        """ _dest (int): 
        The current destination of the vehicle.
        If the vehicle does not have a destination, _dest is None. """
        self._dest = None
        """ _path (list(node)): 
        It might be interesting to remember the 
        paths of all vehicles in the simulation. """
        self._path = []



