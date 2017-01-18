class Package:
    """
    A package is the item being moved around the world space graph.
    It has a starting position, _src, and a destination, _dest.
    A solution to the search problem has all packages at their 
    destinations.  They can only get there by being carried by
    Vehicles.
    """
    def __init__(self, new_id, src, dest):
        """
        :param new_id: The unique id of the package
        :type new_id: int
        :param src: The starting location of this package.
        :type src: int
        :param dest: The destination location of this package.
        :type dest: int
        """
        
        _id = new_id
        _src = src
        _dest = dest
        """ _vehicle (int):
        The vehicle currently carrying this package.  If this
        package is not being held, _vehicle is None. """
        _vehicle = None

    def getId(self):
        return self._id

    def getSrc(self):
        return self._src

    def getDest(self):
        return self._dest

    def isHeld(self):
        return True is self._vehicle is None else False

    def getVehicle(self):
        return self._vehicle
        
