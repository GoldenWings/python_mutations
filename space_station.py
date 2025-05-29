"""
Space Station Module

A 3D space station simulation that supports:
- 3D movement and rotation
- Power management
- Module docking/undocking
- Command execution
"""


class SpaceStation(object):
    """
    A space station that can move in 3D space, rotate, manage power,
    and dock with various modules.
    """

    def __init__(self, x, y, z, facing):
        """
        Initialize a space station at the given position and orientation.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            facing (str): Initial facing direction ("N", "E", "S", "W")
        """
        self.facing = facing
        self.position = (x, y, z)
        self.power_on = True
        self.docked_modules = []
        self.max_modules = 4

    def execute_commands(self, commands):
        """
        Execute a sequence of space-separated commands.

        Args:
            commands (str): Space-separated command string
        """
        for command in commands.split():
            self.execute(command)

    def execute(self, command):
        """
        Execute a single command.

        Args:
            command (str): Command to execute
                - R: Rotate right
                - L: Rotate left
                - F: Move forward
                - B: Move backward
                - U: Move up
                - D: Move down
                - P: Toggle power
                - DOCK_[MODULE]: Dock module
                - UNDOCK_[MODULE]: Undock module
        """
        if not self.power_on and command != "P":
            return  # Cannot execute commands when power is off

        if command == "R":
            self._rotate_right()
        elif command == "L":
            self._rotate_left()
        elif command == "F":
            self._move_forward()
        elif command == "B":
            self._move_backward()
        elif command == "U":
            self._move_up()
        elif command == "D":
            self._move_down()
        elif command == "P":
            self._toggle_power()
        elif command.startswith("DOCK_"):
            module_type = command.split("_")[1]
            self._dock_module(module_type)
        elif command.startswith("UNDOCK_"):
            module_type = command.split("_")[1]
            self._undock_module(module_type)

    def _rotate_right(self):
        """Rotate the station 90 degrees clockwise."""
        rotations = {"N": "E", "E": "S", "S": "W", "W": "N"}
        self.facing = rotations[self.facing]

    def _rotate_left(self):
        """Rotate the station 90 degrees counter-clockwise."""
        rotations = {"N": "W", "W": "S", "S": "E", "E": "N"}
        self.facing = rotations[self.facing]

    def _move_forward(self):
        """Move one unit forward in the current facing direction."""
        x, y, z = self.position
        if self.facing == "N":
            self.position = (x, y + 1, z)
        elif self.facing == "E":
            self.position = (x + 1, y, z)
        elif self.facing == "S":
            self.position = (x, y - 1, z)
        elif self.facing == "W":
            self.position = (x - 1, y, z)

    def _move_backward(self):
        """Move one unit backward from the current facing direction."""
        x, y, z = self.position
        if self.facing == "N":
            self.position = (x, y - 1, z)
        elif self.facing == "E":
            self.position = (x - 1, y, z)
        elif self.facing == "S":
            self.position = (x, y + 1, z)
        elif self.facing == "W":
            self.position = (x + 1, y, z)

    def _move_up(self):
        """Move one unit up in the Z-axis."""
        x, y, z = self.position
        self.position = (x, y, z + 1)

    def _move_down(self):
        """Move one unit down in the Z-axis."""
        x, y, z = self.position
        self.position = (x, y, z - 1)

    def _toggle_power(self):
        """Toggle the power state of the station."""
        self.power_on = not self.power_on

    def _dock_module(self, module_type):
        """
        Dock a module to the station if there's space and it's not already docked.

        Args:
            module_type (str): Type of module to dock
        """
        if len(self.docked_modules) < self.max_modules:
            if module_type not in self.docked_modules:
                self.docked_modules.append(module_type)

    def _undock_module(self, module_type):
        """
        Undock a module from the station if it's currently docked.

        Args:
            module_type (str): Type of module to undock
        """
        if module_type in self.docked_modules:
            self.docked_modules.remove(module_type)
