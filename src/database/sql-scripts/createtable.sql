CREATE TABLE locations (
    idlocations int NOT NULL,
    sitename    varchar(60),
    PRIMARY KEY (idlocations)
);

CREATE TABLE inventory (
    idinventory int NOT NULL,
    itemName    varchar(60),
    amount      int,
    idlocations int,
    PRIMARY KEY (idinventory),
    FOREIGN KEY (idlocations) REFERENCES locations(idlocations)
);