from Vehicle import Vehicle
from Package import Package

if __name__ == "__main__":
    print("Hello.")

    packages = []
    vehicles = []

    for i in range(10):
        vehicles.append(Vehicle(i, i))
        packages.append(Package(i, i, i))

