CREATE TABLE locations (
    id int NOT NULL,
    name    varchar(60),
    PRIMARY KEY (id)
);

CREATE TABLE ingredients (
    id int NOT NULL,
    name    varchar(60),
    amount      int,
    location_id int,
    PRIMARY KEY (id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);
