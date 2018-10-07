class Map(object):
    """ Stores details on a map. """

    def __init__(self, name, filepath):
        self.name = name
        self.filepath = filepath


class MapStore(object):
    """ MapStore stores all the maps for DALSys. """

    def __init__(self, conn=None):
        self._maps = {}
        self._conn = conn

    def add(self, a_map):
        """ Adds a new map to the store. """
        if a_map.name in self._maps:
            raise Exception('Map already exists in store')
        else:
            self._maps[a_map.name] = a_map

    def remove(self, a_map):
        """ Removes a map from the store. """
        if not a_map.name in self._maps:
            raise Exception('Map does not exist in store')
        else:
            del self._maps[a_map.name]

    def get(self, name):
        """ Retrieves a map from the store by its name. """
        if not name in self._maps:
            return None
        else:
            return self._maps[name]

    def list_all(self):
        """ Lists all the maps in the store. """
        name_list = []
        for key in self._maps:
            name_list.append(key)
        return name_list

    def save(self):
        """ Saves the store to the database. """
        pass    # TODO: we don't have a database yet
