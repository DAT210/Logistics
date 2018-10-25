CREATE TABLE location (
    id int NOT NULL,
    name    varchar(60),
    PRIMARY KEY (id)
);

CREATE TABLE ingredient (
    id int NOT NULL,
    name    varchar(60),
    amount      int,
    locationID int,
    PRIMARY KEY (id),
    FOREIGN KEY (locationID) REFERENCES location(id)
);