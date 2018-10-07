import unittest
from datetime import date
from operators import Operator, OperatorStore

class OperatorTest(unittest.TestCase):
    def test_pass_all(self):
        # Arrange
        op = Operator()
        op.first_name = "Matthew"
        op.date_of_birth = date(1995, 12, 25)
        op.drone_license = 2
        op.rescue_endorsement = True
        op.operations = 5
        store = OperatorStore()

        # Act
        act = store.add(op)

        # Assert
        self.assertTrue(act.is_valid())

    def test_fail_name(self):
        # Arrange
        op = Operator()
        op.date_of_birth = date(1995, 12, 25)
        op.drone_license = 1
        store = OperatorStore()

        # Act
        act = store.add(op)

        # Assert
        self.assertFalse(act.is_valid())

    def test_fail_dob(self):
        # Arrange
        op = Operator()
        op.first_name = "Matthew"
        op.drone_license = 1
        store = OperatorStore()

        # Act
        act = store.add(op)

        # Assert
        self.assertFalse(act.is_valid())

    def test_fail_license(self):
        # Arrange
        op = Operator()
        op.first_name = "Matthew"
        op.date_of_birth = date(1995, 12, 25)
        store = OperatorStore()

        # Act
        act = store.add(op)

        # Assert
        self.assertFalse(act.is_valid())

    def test_fail_class2(self):
        # Arrange
        op = Operator()
        op.first_name = "Matthew"
        op.date_of_birth = date(2005, 12, 25)
        op.drone_license = 2
        store = OperatorStore()

        # Act
        act = store.add(op)

        # Assert
        self.assertFalse(act.is_valid())

    def test_fail_endorsement(self):
        # Arrange
        op = Operator()
        op.first_name = "Matthew"
        op.date_of_birth = date(1995, 12, 25)
        op.drone_license = 1
        op.rescue_endorsement = True
        store = OperatorStore()

        # Act
        act = store.add(op)

        # Assert
        self.assertFalse(act.is_valid())

    def test_add(self):
        # Arrange
        op = Operator()
        op.first_name = "Matthew"
        op.date_of_birth = date(1995, 12, 25)
        op.drone_license = 2
        op.rescue_endorsement = True
        op.operations = 5
        store = OperatorStore()

        # Act
        act = store.add(op)
        act.commit()

        # Assert
        self.assertEqual(store.get(1), op)
        
if __name__ == '__main__':
    unittest.main()
