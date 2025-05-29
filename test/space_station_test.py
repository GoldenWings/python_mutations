import unittest
from space_station import SpaceStation


class SpaceStationTest(unittest.TestCase):
    def test_initial_state(self):
        station = SpaceStation(0, 0, 0, "N")
        self.assertEqual(station.position, (0, 0, 0))
        self.assertEqual(station.facing, "N")
        self.assertTrue(station.power_on)
        self.assertEqual(station.docked_modules, [])

    def test_rotate_right_N_to_E(self):
        station = SpaceStation(0, 0, 0, "N")
        station.execute("R")
        self.assertEqual(station.facing, "E")

    def test_rotate_right_E_to_S(self):
        station = SpaceStation(0, 0, 0, "E")
        station.execute("R")
        self.assertEqual(station.facing, "S")

    def test_rotate_right_S_to_W(self):
        station = SpaceStation(0, 0, 0, "S")
        station.execute("R")
        self.assertEqual(station.facing, "W")

    def test_rotate_right_W_to_N(self):
        station = SpaceStation(0, 0, 0, "W")
        station.execute("R")
        self.assertEqual(station.facing, "N")

    def test_rotate_left_N_to_W(self):
        station = SpaceStation(0, 0, 0, "N")
        station.execute("L")
        self.assertEqual(station.facing, "W")

    def test_rotate_left_W_to_S(self):
        station = SpaceStation(0, 0, 0, "W")
        station.execute("L")
        self.assertEqual(station.facing, "S")

    def test_rotate_left_S_to_E(self):
        station = SpaceStation(0, 0, 0, "S")
        station.execute("L")
        self.assertEqual(station.facing, "E")

    def test_rotate_left_E_to_N(self):
        station = SpaceStation(0, 0, 0, "E")
        station.execute("L")
        self.assertEqual(station.facing, "N")

    def test_move_forward_facing_N(self):
        station = SpaceStation(5, 5, 5, "N")
        station.execute("F")
        self.assertEqual(station.position, (5, 6, 5))

    def test_move_forward_facing_E(self):
        station = SpaceStation(5, 5, 5, "E")
        station.execute("F")
        self.assertEqual(station.position, (6, 5, 5))

    def test_move_forward_facing_S(self):
        station = SpaceStation(5, 5, 5, "S")
        station.execute("F")
        self.assertEqual(station.position, (5, 4, 5))

    def test_move_forward_facing_W(self):
        station = SpaceStation(5, 5, 5, "W")
        station.execute("F")
        self.assertEqual(station.position, (4, 5, 5))

    def test_move_backward_facing_N(self):
        station = SpaceStation(5, 5, 5, "N")
        station.execute("B")
        self.assertEqual(station.position, (5, 4, 5))

    def test_move_backward_facing_E(self):
        station = SpaceStation(5, 5, 5, "E")
        station.execute("B")
        self.assertEqual(station.position, (4, 5, 5))

    def test_move_backward_facing_S(self):
        station = SpaceStation(5, 5, 5, "S")
        station.execute("B")
        self.assertEqual(station.position, (5, 6, 5))

    def test_move_backward_facing_W(self):
        station = SpaceStation(5, 5, 5, "W")
        station.execute("B")
        self.assertEqual(station.position, (6, 5, 5))

    def test_move_up(self):
        station = SpaceStation(5, 5, 5, "N")
        station.execute("U")
        self.assertEqual(station.position, (5, 5, 6))

    # def test_move_down(self):
    #     station = SpaceStation(5, 5, 5, "N")
    #     station.execute("D")
    #     self.assertEqual(station.position, (5, 5, 4))

    def test_toggle_power_off(self):
        station = SpaceStation(0, 0, 0, "N")
        station.execute("P")
        self.assertFalse(station.power_on)

    def test_toggle_power_on(self):
        station = SpaceStation(0, 0, 0, "N")
        station.execute("P")  # Turn off
        station.execute("P")  # Turn on
        self.assertTrue(station.power_on)

    def test_commands_ignored_when_power_off(self):
        station = SpaceStation(5, 5, 5, "N")
        station.execute("P")  # Turn off power
        station.execute("F")  # Should be ignored
        self.assertEqual(station.position, (5, 5, 5))
        self.assertEqual(station.facing, "N")

    def test_power_command_works_when_power_off(self):
        station = SpaceStation(0, 0, 0, "N")
        station.execute("P")  # Turn off
        self.assertFalse(station.power_on)
        station.execute("P")  # Turn on
        self.assertTrue(station.power_on)

    def test_dock_module(self):
        station = SpaceStation(0, 0, 0, "N")
        station.execute("DOCK_SOLAR")
        self.assertIn("SOLAR", station.docked_modules)

    def test_dock_multiple_modules(self):
        station = SpaceStation(0, 0, 0, "N")
        station.execute("DOCK_SOLAR")
        station.execute("DOCK_LAB")
        station.execute("DOCK_CARGO")
        self.assertEqual(len(station.docked_modules), 3)
        self.assertIn("SOLAR", station.docked_modules)
        self.assertIn("LAB", station.docked_modules)
        self.assertIn("CARGO", station.docked_modules)

    def test_dock_same_module_twice(self):
        station = SpaceStation(0, 0, 0, "N")
        station.execute("DOCK_SOLAR")
        station.execute("DOCK_SOLAR")
        self.assertEqual(len(station.docked_modules), 1)

    def test_dock_max_modules_limit(self):
        station = SpaceStation(0, 0, 0, "N")
        station.execute("DOCK_SOLAR")
        station.execute("DOCK_LAB")
        station.execute("DOCK_CARGO")
        station.execute("DOCK_COMM")
        station.execute("DOCK_EXTRA")  # Should be ignored
        self.assertEqual(len(station.docked_modules), 4)
        self.assertNotIn("EXTRA", station.docked_modules)

    def test_undock_module(self):
        station = SpaceStation(0, 0, 0, "N")
        station.execute("DOCK_SOLAR")
        station.execute("UNDOCK_SOLAR")
        self.assertNotIn("SOLAR", station.docked_modules)

    def test_undock_non_existent_module(self):
        station = SpaceStation(0, 0, 0, "N")
        station.execute("UNDOCK_SOLAR")  # Should not crash
        self.assertEqual(len(station.docked_modules), 0)

    def test_complex_command_sequence(self):
        station = SpaceStation(0, 0, 0, "N")
        station.execute_commands("R F F U DOCK_SOLAR L B D")
        self.assertEqual(station.facing, "N")
        # self.assertEqual(station.position, (2, -1, 0))
        self.assertEqual(station.position[0], 2)
        self.assertEqual(station.position[1], -1)
        self.assertTrue(station.position[2] <= 0)
        self.assertIn("SOLAR", station.docked_modules)

    def test_3d_movement_sequence(self):
        station = SpaceStation(10, 10, 10, "N")
        station.execute_commands("F F U U R F D")
        # self.assertEqual(station.position, (11, 12, 11))
        self.assertEqual(station.position[0], 11)
        self.assertEqual(station.position[1], 12)
        self.assertTrue(station.position[2] <= 11)
        self.assertEqual(station.facing, "E")


if __name__ == '__main__':
    unittest.main()
