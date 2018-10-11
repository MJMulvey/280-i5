class Drone(object):
    """ Stores details on a drone. """

    def __init__(self, id=-1, name="<new>", class_type=1, rescue="No", operator="<None>", mapID=-1):
        self.id = id
        self.name = name
        if (class_type == 1):
            self.class_type = "One"
        elif (class_type == 2):
            self.class_type = "Two"
        else:
            self.class_type = "Invalid Class"
        self.rescue = rescue
        self.operator = operator
        self.location = (0, 0)
        self.map = mapID


class DroneAction(object):
    """ A pending action on the DroneStore. """

    def __init__(self, drone, operator, commit_action):
        self.drone = drone
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

        self._commit_action(self.drone, self.operator)
        self._committed = True


class DroneStore(object):
    """ DroneStore stores all the drones for DALSys. """

    def __init__(self, conn=None):
        self._drones = {}
        self._conn = conn
        if (self._conn != None):
            cursor = conn.cursor()
            query = "SELECT d.id, d.name, d.class, CASE WHEN d.rescue = 1 THEN 'Yes' ELSE 'No' END AS rescue, IFNULL(op.firstName, '<None>'), IFNULL(op.lastName, ''), d.mapID FROM Drone d LEFT OUTER JOIN Operator op ON d.operatorID = op.id"
            cursor.execute(query)
            for (id, name, classStr, rescue, opName1, opName2, mapID) in cursor:
                drone = Drone(id, name, classStr, rescue, opName1 + " " + opName2, mapID)
                self.add(drone)
            cursor.close()

    def add(self, drone):
        """ Adds a new drone to the store. """
        if drone.id in self._drones:
            raise Exception('Drone already exists in store')
        else:
            self._drones[drone.id] = drone

    def remove(self, drone):
        """ Removes a drone from the store. """
        if not drone.id in self._drones:
            raise Exception('Drone does not exist in store')
        else:
            del self._drones[drone.id]

    def get(self, id):
        """ Retrieves a drone from the store by its ID. """
        if not id in self._drones:
            return None
        else:
            return self._drones[id]

    def list_all(self):
        """ Lists all the drones in the system. """
        for drone in self._drones:
            yield self._drones[drone]

    def allocate(self, drone, operator):
        """ Starts the allocation of a drone to an operator. """
        action = DroneAction(drone, operator, self._allocate)
        if operator.drone is not None: 
            action.add_message("Operator can only control one drone")
        if drone.class_type == 2 and operator.drone_license == 1:
            action.add_message("Operator does not have correct drone license")
        if drone.rescue and operator.rescue_endorsement == False:
            action.add_message("Operator does not have rescue endorsement")
        return action

    def _allocate(self, drone, operator):
        """ Performs the actual allocation of the operator to the drone. """
        if operator.drone is not None:
            # If the operator had a drone previously, we need to clean it so it does not
            # hold an incorrect reference
            operator.drone.operator = None
        operator.drone = drone
        drone.operator = operator
        self.save(drone)

    def save(self, drone):
        """ Saves the drone to the database. """
        if (drone.id != -1):
            droneID = drone.id
            name = drone.name
            if (drone.class_type == "One"):
                classInt = 1
            elif (drone.class_type == "Two"):
                classInt = 2
            else:
                classInt = 0
            if (drone.rescue == "Yes"):
                rescue = 1
            else:
                rescue = 0
            if (self._conn != None):
                cursor = self._conn.cursor()
                query = "UPDATE Drone SET name='%s', class=%s, rescue=%s WHERE id = %s;" % (name, classInt, rescue, droneID)
                cursor.execute(query)
                cursor.close()
        else:
            name = drone.name
            if (drone.class_type == "One"):
                classInt = 1
            elif (drone.class_type == "Two"):
                classInt = 2
            else:
                classInt = 0
            if (drone.rescue == "Yes"):
                rescue = 1
            else:
                rescue = 0
            if (self._conn != None):
                cursor = self._conn.cursor()
                query = "INSERT INTO Drone (name, class, rescue) VALUES ('%s', %s, %s);" % (name, classInt, rescue)
                cursor.execute(query)
                cursor.close()