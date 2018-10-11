class Map(object):
    """ Stores details on a map. """

    def __init__(self, id, name, filepath):
        self.id = id
        self.name = name
        self.filepath = filepath


class MapStore(object):
    """ MapStore stores all the maps for DALSys. """

    def __init__(self, conn=None):
        self._maps = {}
        self._conn = conn
        if (self._conn != None):
            cursor = conn.cursor()
            query = "SELECT id, name, filePath FROM Map"
            cursor.execute(query)
            for (id, name, filePath) in cursor:
                map = Map(id, name, filePath)
                self.add(map)
            cursor.close()

    def add(self, a_map):
        """ Adds a new map to the store. """
        if a_map.id in self._maps:
            raise Exception('Map already exists in store')
        else:
            self._maps[a_map.id] = a_map

    def remove(self, a_map):
        """ Removes a map from the store. """
        if not a_map.id in self._maps:
            raise Exception('Map does not exist in store')
        else:
            del self._maps[a_map.id]

    def get(self, id):
        """ Retrieves a map from the store by its id. """
        if not id in self._maps:
            return None
        else:
            return self._maps[id]

    def list_all(self):
        """ Lists all the maps in the store. """
        id_list = []
        for key in self._maps:
            name_list.append(key)
        return id_list

    def save(self):
        """ Saves the store to the database. """
        pass    # TODO: we don't have a database yet
