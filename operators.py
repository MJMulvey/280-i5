from datetime import date

class Operator(object):
    """ Stores details on an operator. """

    def __init__(self, id=0, first_name="<new>", family_name=None, date_of_birth=None, drone_license=None, rescue_endorsement=None, operations=0, drone="<None>"):
        self.id = id
        self.first_name = first_name
        self.family_name = family_name
        self.date_of_birth = date_of_birth
        self.drone_license = drone_license
        self.rescue_endorsement = rescue_endorsement
        self.operations = operations
        self.drone = drone


class OperatorAction(object):
    """ A pending action on the OperatorStore. """

    def __init__(self, operator, commit_action):
        self.operator = operator
        self.messages = []
        self._commit_action = commit_action
        self._committed = False

    def add_message(self, message):
        """ Adds a message to the action. """
        self.messages.append(message)

    def is_valid(self):
        """ Returns True if the action is valid, False otherwise. """
        return len(self.messages) == 0

    def commit(self):
        """ Commits (performs) this action. """
        if self._committed:
            raise Exception("Action has already been committed")

        self._commit_action(self.operator)
        self._committed = True


class OperatorStore(object):
    """ Stores the operators. """

    def __init__(self, conn=None):
        self._operators = {}
        self._conn = conn
        if (self._conn != None):
            cursor = conn.cursor()
            query = "SELECT op.id, op.firstName, op.lastName, op.dateOfBirth, CASE WHEN op.license = 1 THEN 'One' WHEN op.license = 2 THEN 'Two' ELSE 'Invalid license' END AS license, CASE WHEN op.rescueEndorsement = 1 THEN 'Yes' ELSE 'No' END AS rescue, op.operations, IFNULL(d.name, '<None>') droneName, IFNULL(d.id, '') droneID FROM Operator op LEFT OUTER JOIN Drone d ON d.operatorID = op.id"
            cursor.execute(query)
            for (id, firstName, lastName, dateOfBirth, license, rescue, operations, droneName, droneID) in cursor:
                if (droneID == ""):
                    operator = Operator(id, firstName, lastName, dateOfBirth, license, rescue, operations,droneName)
                else:
                    operator = Operator(id, firstName, lastName, dateOfBirth, license, rescue, operations, droneID + ": " + droneName)
                self.add(operator)
            cursor.close()

    def add(self, operator):
        """ Starts adding a new operator to the store. """
        if operator.id in self._operators:
            raise Exception('Operator already exists in store')
        else:
            self._operators[operator.id] = operator
        """
        action = OperatorAction(operator, self._add)
        check_age = True
        if operator.first_name is None:
            action.add_message("First name is required")
        if operator.date_of_birth is None:
            action.add_message("Date of birth is required")
            check_age = False
        if operator.drone_license is None:
            action.add_message("Drone license is required")
        else:
            if check_age and operator.drone_license == 2:
                today = date.today()
                age = today.year - operator.date_of_birth.year - \
                    ((today.month, today.day) < (
                        operator.date_of_birth.month, operator.date_of_birth.day))
                if age < 20:
                    action.add_message(
                        "Operator should be at least twenty to hold a class 2 license")
        if operator.rescue_endorsement == "Yes" and operator.operations < 5:
            action.add_message("Operator must have been involved in five prior rescure operations to hold a rescue drone endorsement")
        return action"""

    def _add(self, operator):
        """ Adds a new operator to the store. """
        if operator.id in self._operators:
            raise Exception('Operator already exists in store')
        else:
            self._operators[operator.id] = operator

    def remove(self, operator):
        """ Removes a operator from the store. """
        if not operator.id in self._operators:
            raise Exception('Operator does not exist in store')
        else:
            del self._operators[operator.id]

    def get(self, id):
        """ Retrieves a operator from the store by its ID or name. """
        """if not id in self._operators:
            return None
        else:
            return self._operators[id]"""
        if isinstance(id, basestring):
            for op in self._operators:
                if (op.first_name + ' ' + op.family_name) == id:
                    return op
            return None
        else:
            if not id in self._operators:
                return None
            else:
                return self._operators[id]

    def list_all(self):
        """ Lists all the _operators in the system. """
        for operator in self._operators:
            yield self._operators[operator]

    def save(self):
        """ Saves the store to the database. """
        pass    # TODO: we don't have a database yet
