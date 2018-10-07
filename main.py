import mysql.connector
from drones import Drone, DroneStore

class Application(object):
    """ Main application wrapper for processing input. """

    def __init__(self, conn):
        self._drones = DroneStore(conn)
        self._commands = {
            'list': self.list,
            'add': self.add,
            'update': self.update,
            'remove': self.remove,
            'allocate': self.allocate,
            'help': self.help,
        }

    def main_loop(self):
        print 'Welcome to DALSys'
        cont = True
        while cont:
            val = raw_input('> ').strip().lower()
            cmd = None
            args = {}
            if len(val) == 0:
                continue

            try:
                parts = val.split(' ')
                if parts[0] == 'quit':
                    cont = False
                    print 'Exiting DALSys'
                else:
                    cmd = self._commands[parts[0]]
            except KeyError:
                print '!! Unknown command "%s" !!' % (val)

            if cmd is not None:
                args = parts[1:]
                try:
                    cmd(args)
                except Exception as ex:
                    print '!! %s !!' % (str(ex))

    def add(self, args):
        """ Adds a new drone. """
        cursor = conn.cursor()
        query = ""
        if len(args) == 0:
            print "!! name is required !!"
        elif len(args) == 1:
            if args[0][0] == "-":
                print "!! name is required !!"
            else:
                print "!! class is required !!"
        else:
            if args[0][0] == "-":
                print "!! name is required !!"
            elif "class" not in args[1]:
                print "!! class is required !!"
            else:
                name = args[0]
                classNum = int(args[1][-1])
                if classNum == 1 or classNum == 2:
                    if len(args) > 2:
                        if args[2] == "-rescue":
                            rescue = 1
                        else:
                            rescue = 0
                    else:
                        rescue = 0
                    query = "INSERT INTO Drone (name, class, rescue) VALUES (%s, %s, %s);"
                    cursor.execute(query, (name, classNum, rescue))
                    conn.commit()
                    idStr = str(cursor.lastrowid)
                    if rescue == 1:
                        print "Added rescue drone with ID " + "0" * max(0, 4 - len(idStr)) + idStr
                    else:
                        print "Added drone with ID " + "0" * max(0, 4 - len(idStr)) + idStr
                else:
                    print "!! only class values of 1 and 2 are allowed !!"
        cursor.close()

    def allocate(self, args):
        """ Allocates a drone to an operator. """
        raise Exception("Allocate method has not been implemented yet")

    def help(self, args):
        """ Displays help information. """
        print "Valid commands are:"
        print "* list [- class =(1|2)] [- rescue ]"
        print "* add 'name ' -class =(1|2) [- rescue ]"
        print "* update id [- name ='name '] [- class =(1|2)] [- rescue ]"
        print "* remove id"
        print "* allocate id 'operator'"

    def list(self, args):
        """ Lists all the drones in the system. """
        cursor = conn.cursor()
        query = ""
        rescue = False
        classNum = ""
        for index in range (len(args)):
            if "rescue" in args[index]:
                rescue = True
            if "class" in args[index]:
                classNum = int(args[index][-1])
        if rescue == False:
            if classNum == "":
                query = "SELECT d.id, d.name, CASE WHEN d.class = 1 THEN 'One' ELSE 'Two' END AS classStr, CASE WHEN d.rescue = 1 THEN 'Yes' ELSE 'No' END AS rescue, IFNULL(op.firstName, '<none>'), IFNULL(op.lastName, '') FROM Drone d LEFT OUTER JOIN Operator op ON d.operatorID = op.id ORDER BY name"
            elif classNum == 1 or classNum ==2:
                query = "SELECT d.id, d.name, CASE WHEN d.class = 1 THEN 'One' ELSE 'Two' END AS classStr, CASE WHEN d.rescue = 1 THEN 'Yes' ELSE 'No' END AS rescue, IFNULL(op.firstName, '<none>'), IFNULL(op.lastName, '') FROM Drone d LEFT OUTER JOIN Operator op ON d.operatorID = op.id WHERE d.class = %d ORDER BY name" % (classNum)
            else:
                print "Unknown drone class %d" % (classNum)
        else:
            if classNum == "":
                query = "SELECT d.id, d.name, CASE WHEN d.class = 1 THEN 'One' ELSE 'Two' END AS classStr, CASE WHEN d.rescue = 1 THEN 'Yes' ELSE 'No' END AS rescue, IFNULL(op.firstName, '<none>'), IFNULL(op.lastName, '') FROM Drone d LEFT OUTER JOIN Operator op ON d.operatorID = op.id WHERE d.rescue = 1 ORDER BY name"
            elif classNum == 1 or classNum ==2:
                query = "SELECT d.id, d.name, CASE WHEN d.class = 1 THEN 'One' ELSE 'Two' END AS classStr, CASE WHEN d.rescue = 1 THEN 'Yes' ELSE 'No' END AS rescue, IFNULL(op.firstName, '<none>'), IFNULL(op.lastName, '') FROM Drone d LEFT OUTER JOIN Operator op ON d.operatorID = op.id WHERE d.rescue = 1 AND d.class = %d ORDER BY name" % (classNum)
            else:
                print "Unknown drone class %d" % (classNum)
        if query != "":
            cursor.execute(query)
            if cursor.fetchall() == []:
                print "!! There are no drones for this criteria !!"
            else:
                cursor.execute(query)
                print "ID   Name                Class Rescue Operator"
                for (id, name, classStr, rescue, opName1, opName2) in cursor:
                    id = str(id)
                    outString = "0" * max(0, 4 - len(id)) + id + " " + name + " " * max(0, 20 - len(name)) + classStr + " " * 3 + rescue + " " * (7 - len(rescue)) + opName1 + " " + opName2
                    print outString
                if cursor.rowcount == None:
                    print str(cursor.rowcount) + " drone listed"
                else:
                    print str(cursor.rowcount) + " drones listed"
        cursor.close()

    def remove(self, args):
        """ Removes a drone. """
        raise Exception("Remove method has not been implemented yet")

    def update(self, args):
        """ Updates the details for a drone. """
        raise Exception("Update method has not been implemented yet")


if __name__ == '__main__':
    conn = mysql.connector.connect(user='mmul995',
                                    password='iter3pass',
                                    host='studdb-mysql.fos.auckland.ac.nz',
                                    database='stu_mmul995_COMPSCI_280_C_S2_2018',
                                    charset='utf8')
    app = Application(conn)
    app.main_loop()
    conn.close()
