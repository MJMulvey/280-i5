/* Creates the table that will contain the maps from the MapStore */
CREATE TABLE Map (
    id                  INT NOT NULL AUTO_INCREMENT,
    name                VARCHAR(100) NOT NULL,
    filePath            VARCHAR(150),

    PRIMARY KEY (id)
);

/* Creates the table that will contain the operators from the OperatorStore */
CREATE TABLE Operator (
    id                  INT NOT NULL AUTO_INCREMENT,
    firstName           VARCHAR(100) NOT NULL,
    lastName            VARCHAR(100),
    dateOfBirth         DATE NOT NULL,
    license             TINYINT NOT NULL,
    rescueEndorsement   TINYINT NOT NULL,
    operations          SMALLINT NOT NULL,
    droneID             INT UNIQUE,

    PRIMARY KEY (id)
);

/* Creates the table that will contain the drones from the DroneStore */
CREATE TABLE Drone (
    id                  INT NOT NULL AUTO_INCREMENT,
    name                VARCHAR(100) NOT NULL,
    class               TINYINT NOT NULL,
    rescue              TINYINT NOT NULL,
    operatorID          INT UNIQUE,
    mapID               INT,

    PRIMARY KEY (id),
    FOREIGN KEY (operatorID) REFERENCES Operator(id),
    FOREIGN KEY (mapID) REFERENCES Map(id)
);

/* Adds the foreign key to the Operator table that references the Drone table's PK. This was not added when the Operator table was created as the Drone table had not been created yet. */
ALTER TABLE Operator ADD FOREIGN KEY (droneID) REFERENCES Drone(id);