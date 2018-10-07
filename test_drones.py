import unittest
from drones import Drone, DroneStore

class DroneTest(unittest.TestCase):
    def test_add_success(self):
        # Arrange
        dr = Drone("Test drone")
        store = DroneStore()

        # Act
        store.add(dr)

        # Assert
        self.assertEqual(store.get(1), dr)

    def test_add_fail(self):
        # Arrange
        dr = Drone("Test drone")
        store = DroneStore()
        errorText = 'Drone already exists in store'

        # Act
        try:
            store.add(dr)
            store.add(dr)
            
        # Assert
        except Exception as ex:
            self.assertEqual(str(ex), errorText)

    def test_remove_success(self):
        # Arrange
        dr = Drone("Test drone")
        store = DroneStore()
        store.add(dr)

        # Act
        store.remove(dr)

        # Assert
        self.assertEqual(store.get(1), None)

    def test_remove_fail(self):
        # Arrange
        dr = Drone("Test drone")
        store = DroneStore()
        errorText = 'Drone does not exist in store'

        # Act
        try:
            store.remove(dr)
            
        # Assert
        except Exception as ex:
            self.assertEqual(str(ex), errorText)

if __name__ == '__main__':
    unittest.main()
