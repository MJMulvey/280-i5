import unittest
from maps import Map, MapStore

class MapTest(unittest.TestCase):
    def test_add_success(self):
        # Arrange
        mp = Map("Test map", "")
        store = MapStore()

        # Act
        store.add(mp)

        # Assert
        self.assertEqual(store.get("Test map"), mp)

    def test_add_fail(self):
        # Arrange
        mp = Map("Test map", "")
        store = MapStore()
        errorText = 'Map already exists in store'

        # Act
        try:
            store.add(mp)
            store.add(mp)
            
        # Assert
        except Exception as ex:
            self.assertEqual(str(ex), errorText)

    def test_remove_success(self):
        # Arrange
        mp = Map("Test map", "")
        store = MapStore()
        store.add(mp)

        # Act
        store.remove(mp)

        # Assert
        self.assertEqual(store.list_all(), [])

    def test_remove_fail(self):
        # Arrange
        mp = Map("Test map", "")
        store = MapStore()
        errorText = 'Map does not exist in store'

        # Act
        try:
            store.remove(mp)
            
        # Assert
        except Exception as ex:
            self.assertEqual(str(ex), errorText)

    def test_list_all(self):
        # Arrange
        mp1 = Map("Test map 1", "")
        mp2 = Map("Test map 2", "")
        store = MapStore()
        store.add(mp1)
        store.add(mp2)

        # Act
        act = store.list_all()

        #Assert
        self.assertEqual(act, ["Test map 1", "Test map 2"])

    def test_get_success(self):
        # Arrange
        mp = Map("Test map", "")
        store = MapStore()
        store.add(mp)
        
        # Act
        act = store.get("Test map")

        # Assert
        self.assertEqual(act, mp)

    def test_get_fail(self):
        # Arrange
        mp = Map("Test map", "")
        store = MapStore()
        errorText = 'Map does not exist in store'

        # Act
        try:
            store.get(mp)
            
        # Assert
        except Exception as ex:
            self.assertEqual(str(ex), errorText)

if __name__ == '__main__':
    unittest.main()
