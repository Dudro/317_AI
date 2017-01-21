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

    def get_carLoc(self):
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
            sum += 1 if self._packages[i]
        return sum

