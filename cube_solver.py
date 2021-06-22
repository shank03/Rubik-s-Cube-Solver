import kociemba
import numpy as np


# REFERENCE and CREDITS: https://github.com/BijanRegmi/RubikCubeSolver

class Cube:
    def __init__(self):
        """
            Facing reference:
            - WHITE:                    Top = BLUE
            - YELLOW:                   Top = GREEN
            - ORANGE, RED, GREEN, BLUE: Top = WHITE

            Usage
            ```python

                import cube_solver

                cube = cube_solver.Cube()

                # Get the 3x3 data for, let's say white face (white center)
                # from OpenCV
                # IMPORTANT: be careful about mirror image given by camera
                white_data = [['b' 'w' 'y']
                              ['w' 'w' 'y']
                              ['o' 'b' 'r']]

                for i in range(3):
                    for j in range(3):
                        cube.white[i][j] = white_data[i][j]
            ```
        """

        # White center
        self.white = np.array([
            ["w", "w", "w"],
            ["w", "w", "w"],
            ["w", "w", "w"]
        ])

        # Yellow center
        self.yellow = np.array([
            ["y", "y", "y"],
            ["y", "y", "y"],
            ["y", "y", "y"]
        ])

        # Green center
        self.green = np.array([
            ["g", "g", "g"],
            ["g", "g", "g"],
            ["g", "g", "g"]
        ])

        # Blue center
        self.blue = np.array([
            ["b", "b", "b"],
            ["b", "b", "b"],
            ["b", "b", "b"]
        ])

        # Red center
        self.red = np.array([
            ["r", "r", "r"],
            ["r", "r", "r"],
            ["r", "r", "r"]
        ])

        # Orange center
        self.orange = np.array([
            ["o", "o", "o"],
            ["o", "o", "o"],
            ["o", "o", "o"]
        ])

    # Get current state of the cube
    def __current_state(self):
        state = ""
        for i in self.white:
            for j in i:
                state += selectText(j)

        for i in self.red:
            for j in i:
                state += selectText(j)

        for i in self.green:
            for j in i:
                state += selectText(j)

        for i in self.yellow:
            for j in i:
                state += selectText(j)

        for i in self.orange:
            for j in i:
                state += selectText(j)

        for i in self.blue:
            for j in i:
                state += selectText(j)
        return state

    # Returns the moves to be followed for solving the cube
    def getSolvingSteps(self):
        return kociemba.solve(self.__current_state())


# Convert to kociemba format
def selectText(c):
    f = {
        "w": "U",
        "r": "R",
        "y": "D",
        "o": "L",
        "g": "F",
        "b": "B",
    }.get(c)
    return f
