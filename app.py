"""py -2 -m pip install --user mysql-connector-python"""

import mysql.connector
import Tkinter as tk
import ttk

from drones import Drone, DroneStore
from operators import Operator, OperatorStore
from trackingsystem import TrackingSystem, DroneLocation
from maps import Map, MapStore

class Application(object):
    """ Main application view - displays the menu. """

    def __init__(self, conn):
        # Initialise the stores
        self.drones = DroneStore(conn)
        self.operators = OperatorStore(conn)
        self.tracking = TrackingSystem()
        self.maps = MapStore(conn)

        # Initialise the GUI window
        self.root = tk.Tk()
        self.root.title('Drone Allocation and Localisation')
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Add in the buttons
        drone_button = tk.Button(
            frame, text="View Drones", command=self.view_drones, width=40, padx=5, pady=5)
        drone_button.pack(side=tk.TOP)
        operator_button = tk.Button(
            frame, text="View Operators", command=self.view_operators, width=40, padx=5, pady=5)
        operator_button.pack(side=tk.TOP)
        map_button = tk.Button(
            frame, text="View Map", command=self.view_map, width=40, padx=5, pady=5)
        map_button.pack(side=tk.TOP)
        exit_button = tk.Button(frame, text="Exit System",
                                command=quit, width=40, padx=5, pady=5)
        exit_button.pack(side=tk.TOP)

    def main_loop(self):
        """ Main execution loop - start Tkinter. """
        self.root.mainloop()

    def view_operators(self):
        """ Display the operators. """
        wnd = OperatorListWindow(self)
        self.root.wait_window(wnd.root)

    def view_drones(self):
        """ Display the drones. """
        wnd = DroneListWindow(self)
        self.root.wait_window(wnd.root)

    def view_map(self):
        """ Display the maps. """
        wnd = MapWindow(self)
        self.root.wait_window(wnd.root)

class MapWindow(object):
    """ Window to view maps """

    def __init__(self, parent):
        
        # Add a variable to hold the stores
        self.maps = parent.maps
        self.drones = parent.drones
        self.tracking = parent.tracking

        map_names = self.maps.list_all()

        # Initialise the new top-level window (modal dialog)
        self._parent = parent.root
        self.root = tk.Toplevel(parent.root)
        self.root.title("Map Viewer")
        self.root.transient(parent.root)
        self.root.grab_set()

        # Initialise the top level frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH,
                        expand=tk.Y, padx=10, pady=10)

        # Add in the widgets
        tk.mapString = tk.StringVar()
        
        top_frame = tk.Frame(self.root, width=500, height=100)
        top_frame.grid(in_=self.frame, row=0, column=0, sticky=tk.W)

        add_label = tk.Label(top_frame, text="Map:", padx=15, pady=5)
        add_label.grid(in_=top_frame, row=0, column=0, sticky=tk.W)

        self.add_menu = ttk.Combobox(top_frame, values=(map_names), width=50, textvariable=tk.mapString)
        self.add_menu.insert(tk.END, map_names[0])
        self.add_menu.grid(in_=top_frame, row=0, column=1, sticky=tk.W)
        
        self.canvas = tk.Canvas(self.frame, width=600, height=400)
        self.canvas.grid(in_=self.frame, row=1, column=0, sticky=tk.W)

        self.horizontal_scroll = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.vertical_scroll = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)

        mapName = tk.mapString.get()
        self.map = self.maps.getByName(mapName)
        self.canvas.img = tk.PhotoImage(file=self.map.filepath)

        self.canvas.config(xscrollcommand=self.horizontal_scroll.set, yscrollcommand=self.vertical_scroll.set, scrollregion=(0,0, self.canvas.img.width(), self.canvas.img.height()))

        self.horizontal_scroll.grid(in_=self.frame, row=2, column=0, columnspan=2, sticky=tk.EW)
        self.vertical_scroll.grid(in_=self.frame, row=1, column=2, sticky=tk.NS)

        self.initialise_map(tk.mapString.get())
        self.add_menu.bind('<<ComboboxSelected>>', self.display_map)

        exit_button = tk.Button(self.frame, text="Refresh", command=self.initialise_map(tk.mapString.get()), width=20, padx=5, pady=5)
        exit_button.grid(in_=self.frame, row=3, column=0, sticky=tk.E)

        exit_button = tk.Button(self.frame, text="Close", command=self.close, width=20, padx=5, pady=5)
        exit_button.grid(in_=self.frame, row=4, column=0, sticky=tk.E)

    def initialise_map(self, mapName):
        """ Displays the selected map in the canvas. """
        self.map = self.maps.getByName(mapName)
        mapID = self.map.id
        self.canvas.img = tk.PhotoImage(file=self.map.filepath)
        self.canvas.create_image(0, 0, image=self.canvas.img, anchor=tk.NW)
        
        dronesList = self.drones.list_by_map(mapID)

        for drone in dronesList:
            droneMap = self.maps.get(drone.map)
            drone.location = self.tracking.retrieve(droneMap, drone)
            position = drone.location.position()
            xpos = position[0] * (self.canvas.img.width() / 100)
            ypos = position[1] * (self.canvas.img.height() / 100)
            if (drone.rescue == "Yes"):
                self.canvas.create_oval(xpos - 10, ypos - 10, xpos + 10, ypos + 10, fill='blue')
            else:
                self.canvas.create_oval(xpos - 10, ypos - 10, xpos + 10, ypos + 10, fill='red')
    
    def display_map(self, event):
        """ Updates the map to match the combobox selection. """
        #self.canvas.delete("all")
        mapName = tk.mapString.get()
        self.map = self.maps.getByName(mapName)
        mapID = self.map.id
        self.canvas.img = tk.PhotoImage(file=self.map.filepath)
        self.canvas.create_image(0, 0, image=self.canvas.img, anchor=tk.NW)
        self.canvas.config(xscrollcommand=self.horizontal_scroll.set, yscrollcommand=self.vertical_scroll.set, scrollregion=(0,0, self.canvas.img.width(), self.canvas.img.height()))

        dronesList = self.drones.list_by_map(mapID)
        
        for drone in dronesList:
            droneMap = self.maps.get(drone.map)
            drone.location = self.tracking.retrieve(droneMap, drone)
            position = drone.location.position()
            xpos = position[0] * (self.canvas.img.width() / 100)
            ypos = position[1] * (self.canvas.img.height() / 100)
            if (drone.rescue == "Yes"):
                self.canvas.create_oval(xpos - 10, ypos - 10, xpos + 10, ypos + 10, fill='blue')
            else:
                self.canvas.create_oval(xpos - 10, ypos - 10, xpos + 10, ypos + 10, fill='red')

    def close(self):
        """ Closes the map window. """
        self.root.destroy()

class ListWindow(object):
    """ Base list window. """

    def __init__(self, parent, title):
        # Add a variable to hold the stores
        self.drones = parent.drones
        self.operators = parent.operators
        self.tracking = parent.tracking
        self.maps = parent.maps

        # Initialise the new top-level window (modal dialog)
        self._parent = parent.root
        self.root = tk.Toplevel(parent.root)
        self.root.title(title)
        self.root.transient(parent.root)
        self.root.grab_set()

        # Initialise the top level frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH,
                        expand=tk.Y, padx=10, pady=10)

    def add_list(self, columns, edit_action):
        # Add the list
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.title())
        ysb = ttk.Scrollbar(self.frame, orient=tk.VERTICAL,
                            command=self.tree.yview)
        xsb = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL,
                            command=self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set
        self.tree.bind("<Double-1>", edit_action)

        # Add tree and scrollbars to frame
        self.tree.grid(in_=self.frame, row=0, column=0, sticky=tk.NSEW)
        ysb.grid(in_=self.frame, row=0, column=1, sticky=tk.NS)
        xsb.grid(in_=self.frame, row=1, column=0, sticky=tk.EW)

        # Set frame resize priorities
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def close(self):
        """ Closes the list window. """
        self.root.destroy()


class DroneListWindow(ListWindow):
    """ Window to display a list of drones. """

    def __init__(self, parent):
        super(DroneListWindow, self).__init__(parent, 'Drones')

        # Add the list and fill it with data
        columns = ('id', 'name', 'class', 'rescue', 'operator')
        self.add_list(columns, self.edit_drone)
        self.populate_data()

        # Add the command buttons
        add_button = tk.Button(self.frame, text="Add Drone",
                               command=self.add_drone, width=20, padx=5, pady=5)
        add_button.grid(in_=self.frame, row=2, column=0, sticky=tk.E)
        exit_button = tk.Button(self.frame, text="Close",
                                command=self.close, width=20, padx=5, pady=5)
        exit_button.grid(in_=self.frame, row=3, column=0, sticky=tk.E)

    def populate_data(self):
        """ Populates the data in the view. """
        self.tree.delete(*self.tree.get_children())
        drones = self.drones.list_all()
        for drone in drones:
            self.tree.insert('', 'end', values=(drone.id, drone.name, drone.class_type, drone.rescue, drone.operator))

    def add_drone(self):
        """ Starts a new drone and displays it in the list."""
        # Start a new drone instance
        drone = Drone()
        
        # Display the drone
        self.view_drone(drone, self._save_new_drone)

    def _save_new_drone(self, drone):
        """ Saves the drone in the store and updates the list. """
        self.drones.add(drone)
        self.drones.save(drone)
        self.populate_data()

    def edit_drone(self, event):
        """ Retrieves the drone and shows it in the editor. """
        # Retrieve the identifer of the drone
        item = self.tree.item(self.tree.focus())
        item_id = item['values'][0]

        # Load the drone from the store
        drone = self.drones.get(item_id)

        # Display the drone
        self.view_drone(drone, self._update_drone)

    def _update_drone(self, drone):
        """ Saves the new details of the drone. """
        self.drones.save(drone)
        self.populate_data()

    def view_drone(self, drone, save_action):
        """ Displays the drone editor. """
        wnd = DroneEditorWindow(self, drone, save_action)
        self.root.wait_window(wnd.root)


class OperatorListWindow(ListWindow):
    """ Window to display a list of operators. """

    def __init__(self, parent):
        super(OperatorListWindow, self).__init__(parent, 'Operators')

        # Add the list and fill it with data
        columns = ('name', 'class', 'rescue', 'operations', 'drone')
        self.add_list(columns, self.edit_operator)
        self.populate_data()

        # Add the command buttons
        add_button = tk.Button(self.frame, text="Add Operator",
                               command=self.add_operator, width=20, padx=5, pady=5)
        add_button.grid(in_=self.frame, row=2, column=0, sticky=tk.E)
        exit_button = tk.Button(self.frame, text="Close",
                                command=self.close, width=20, padx=5, pady=5)
        exit_button.grid(in_=self.frame, row=3, column=0, sticky=tk.E)

    def populate_data(self):
        """ Populates the data in the view. """
        self.tree.delete(*self.tree.get_children())
        operators = self.operators.list_all()
        for operator in operators:
            self.tree.insert('', 'end', values=(operator.first_name + " " + operator.family_name, operator.drone_license, operator.rescue_endorsement, operator.operations, operator.drone))

    def add_operator(self):
        """ Starts a new operator and displays it in the list. """
        # Start a new operator instance
        operator = Operator()
        
        # Display the operator
        self.view_operator(operator, self._save_new_operator)

    def _save_new_operator(self, operator):
        """ Saves the operator in the store and updates the list. """
        self.operator.add(operator)
        self.populate_data()

    def edit_operator(self, event):
        """ Retrieves the operator and shows it in the editor. """
        # Retrieve the identifer of the operator
        item = self.tree.item(self.tree.focus())
        item_id = item['values'][0]

        # Load the operator from the store
        operator = self.operators.get(item_id)

        # Display the operator
        self.view_operator(operator, self._update_operator)

    def _update_operator(self, operator):
        """ Saves the new details of the operator. """
        self.operators.save(operator)
        self.populate_data()

    def view_operator(self, operator, save_action):
        """ Displays the operator editor. """
        wnd = OperatorEditorWindow(self, operator, save_action)
        self.root.wait_window(wnd.root)


class EditorWindow(object):
    """ Base editor window. """

    def __init__(self, parent, title, save_action):
        # Initialise the new top-level window (modal dialog)
        self.tracking = parent.tracking
        self.maps = parent.maps

        self._parent = parent.root
        self.root = tk.Toplevel(parent.root)
        self.root.title(title)
        self.root.transient(parent.root)
        self.root.grab_set()

        # Initialise the top level frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH,
                        expand=tk.Y, padx=10, pady=10)

        # Add the editor widgets
        last_row = self.add_editor_widgets()

        # Add the command buttons
        add_button = tk.Button(self.frame, text="Save",
                               command=save_action, width=20, padx=5, pady=5)
        add_button.grid(in_=self.frame, row=last_row + 1, column=1, sticky=tk.E)
        exit_button = tk.Button(self.frame, text="Close",
                                command=self.close, width=20, padx=5, pady=5)
        exit_button.grid(in_=self.frame, row=last_row + 2, column=1, sticky=tk.E)

    def add_editor_widgets(self):
        """ Adds the editor widgets to the frame - this needs to be overriden in inherited classes. 
        This function should return the row number of the last row added - EditorWindow uses this
        to correctly display the buttons. """
        return -1

    def close(self):
        """ Closes the editor window. """
        self.root.destroy()

class DroneEditorWindow(EditorWindow):
    """ Editor window for drones. """

    def __init__(self, parent, drone, save_action):
        self._drone = drone
        self._save_action = save_action

        if (drone.name == None):
            super(DroneEditorWindow, self).__init__(parent, 'Drone: <new>', self.save_drone)
        else:
            name = drone.name
            super(DroneEditorWindow, self).__init__(parent, 'Drone: ' + name, self.save_drone)

    def add_editor_widgets(self):
        """ Adds the widgets for editing a drone. """
        tk.name = tk.StringVar()
        tk.classString = tk.StringVar()
        tk.rescueString = tk.StringVar()
        droneMap = self.maps.get(self._drone.map)
        self._drone.location = self.tracking.retrieve(droneMap, self._drone)

        add_label_name = tk.Label(self.frame, text="Name:", padx=15, pady=5).grid(in_=self.frame, row=0, column=0, sticky=tk.W)

        add_entry = tk.Entry(self.frame, width=50, textvariable=tk.name)
        if (self._drone.name != "<new>"):
            add_entry.insert(tk.END, self._drone.name)
        add_entry.grid(in_=self.frame, row=0, column=1, sticky=tk.W)

        add_label_class = tk.Label(self.frame, text="Drone Class:", padx=15, pady=5).grid(in_=self.frame, row=1, column=0, sticky=tk.W)

        add_menu_class = ttk.Combobox(self.frame, values=("One","Two"), textvariable=tk.classString)
        add_menu_class.insert(tk.END, self._drone.class_type)
        add_menu_class.grid(in_=self.frame, row=1, column=1, sticky=tk.W)

        add_label_rescue = tk.Label(self.frame, text="Rescue Drone:", padx=15, pady=5).grid(in_=self.frame, row=2, column=0, sticky=tk.W)
        
        add_menu_rescue = ttk.Combobox(self.frame, values=("Yes","No"), textvariable=tk.rescueString)
        add_menu_rescue.insert(tk.END, self._drone.rescue)
        add_menu_rescue.grid(in_=self.frame, row=2, column=1, sticky=tk.W)

        add_label_location = tk.Label(self.frame, text="Location", padx=15, pady=5).grid(in_=self.frame, row=3, column=0, sticky=tk.W)
        
        add_location = tk.Entry(self.frame, width=50)
        if (self._drone.location.is_valid()):
            drone_position = self._drone.location.position()
            add_location.insert(tk.END, "(" + str(drone_position[0]) + ", " + str(drone_position[1]) + ")")
        else:
            add_location.insert(tk.END, "n/a")
        add_location.configure(state='readonly')
        add_location.grid(in_=self.frame, row=3, column=1, sticky=tk.W)
        
        return 3

    def save_drone(self):
        """ Updates the drone details and calls the save action. """
        self._drone.name = tk.name.get()
        self._drone.class_type = tk.classString.get()
        self._drone.rescue = tk.rescueString.get()

        self.root.destroy()
        self._save_action(self._drone)


if __name__ == '__main__':
    conn = mysql.connector.connect(user='mmul995',
                                    password='iter3pass',
                                    host='studdb-mysql.fos.auckland.ac.nz',
                                    database='stu_mmul995_COMPSCI_280_C_S2_2018',
                                    charset='utf8')
    app = Application(conn)
    app.main_loop()
    conn.close()
