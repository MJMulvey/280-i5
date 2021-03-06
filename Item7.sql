/* Inserts the data for two maps into the Map table */
INSERT INTO Map (id, name, filePath) 
    VALUES
    (1, "Abel Tasman", "map_abel_tasman_3.gif"),
    (2, "Ruatiti", "map_ruatiti.gif");

/* Inserts the data for four operators into the Operator table */
INSERT INTO Operator (id, firstName, lastName, dateOfBirth, license, rescueEndorsement, operations)
    VALUES
    (1, "Roland", "Deschain", '1990-01-01', 2, 1, 5),
    (2, "Legolas", "Greenleaf", '1985-12-13', 1, 0, 2),
    (3, "Karn", "Liberated", '1989-06-06', 2, 0, 4),
    (4, "Oberyn", "Martell", '1988-07-07', 2, 1, 6);

/* Inserts the data for the unallocated drone into the Drone table */
INSERT INTO Drone (id, name, class, rescue)
    VALUES
    (1, "Drone1", 1, 0),
    (2, "Drone2", 2, 0),
    (3, "Drone3", 2, 1);

/* Inserts the data for the four allocated drones into the Drone table */
INSERT INTO Drone (id, name, class, rescue, operatorID, mapID)
    VALUES

    (4, "Drone4", 2, 1, 4, 1),
    (5, "Drone5", 1, 0, 2, 2);


/* Allocates the four allocated drones to their respecitve operators */
UPDATE Operator SET droneID = 4 WHERE id = 4;
UPDATE Operator SET droneID = 5 WHERE id = 2;
UPDATE Operator SET droneID = 2 WHERE id = 3;
UPDATE Operator SET droneID = 3 WHERE id = 1;