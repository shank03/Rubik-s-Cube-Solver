import scan_cube
import kociemba
from sys import exit
from os import system

sides = scan_cube.scan()
if len(sides) == 6:
    state = ""
    for face in 'URFDLB':
        state += ''.join(sides[face])
    print(state)

    try:
        algo = kociemba.solve(state)

        file = open("Solver/solve.txt", "w")
        file.write(algo)
        file.close()

        # Display 3D simulation
        system("cd Solver && npm run start")
    except ValueError as err:
        print(f"Error: {err}")
        exit(1)

else:
    print("Incomplete")
