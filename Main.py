from Vehicle import Vehicle
from Package import Package
import random

if __name__ == "__main__":

    random.seed(0)

    locations = []
    packages = []
    vehicles = []

    M = 20
    K = 10
    V = 5

    Garage = random.randrange(0, M)

    for i in range(M):
        locations.append(i)
    for i in range(V):
        vehicles.append(Vehicle(i, Garage))
    for i in range(K):
        src = random.randrange(0, M)
        dest = random.randrange(0, M)
        packages.append(Package(i, src, dest))

