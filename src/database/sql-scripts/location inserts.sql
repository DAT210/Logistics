INSERT INTO locations (idlocations, sitename)
VALUES (1, 'Food1');

INSERT INTO locations (idlocations, sitename)
VALUES (2, 'Food2');

INSERT INTO locations (idlocations, sitename)
VALUES (3, 'Food3');


INSERT INTO inventory (idinventory, itemname, amount, idlocations)
VALUES (1, 'Ham', 34, 1);

INSERT INTO inventory (idinventory, itemname, amount, idlocations)
VALUES (2, 'Ham', 21, 2);

INSERT INTO inventory (idinventory, itemname, amount, idlocations)
VALUES (3, 'Ham', 0, 3);

INSERT INTO inventory (idinventory, itemname, amount, idlocations)
VALUES (4, 'Sauce', 24, 1);

INSERT INTO inventory (idinventory, itemname, amount, idlocations)
VALUES (5, 'Sauce', 34, 3);