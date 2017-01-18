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

    def getId(self):
        """
        Return the unique id of this Vehicle.
        :rtype: int
        """
        return self._id

    def getPkg(self):
        """
        Return the contents of this vehicle.  If this Vehicle has
        a package, return the id of that package.  If the vehicle
        is empty, return None.
        :rtype: int, None
        """
        return self._pkg

    def setPkg(self, pkg):
        """
        Pickup a package.  This assigns a package as the contents of
        the vehicle.  Return True if this is successful, and False if
        there is already a package in the vehicle.
        :param pkg: A package id.
        :type pkg: int
        :rtype: bool
        """
        if self._pkg is None:
            self._pkg = pkg
            return True
        else:
            return False

    def dropOffPkg(self):
        """
        Drop off a package.  Because the vehicle does not know all
        about the graph world it drives in, this just means emptying its
        contents.  Return True if successful, and False if the Vehicle
        doesn't have a package to begin with.
        :rtype: bool
        """
        if self._pkg is None:
            return False
        else:
            self._pkg = None
            return True

    def getDest(self):
        """
        Return the current destination of this Vehicle,
        or None if the Vehicle has no destination.
        :rtype: int, None
        """
        return self._dest

    def setDest(self, dest):
        """
        Give this vehicle a current destination.
        """
        self._dest = dest

    def addToPath(self, loc):
        """
        Not sure if this will be any use.
        """
        self._path.append(loc)

