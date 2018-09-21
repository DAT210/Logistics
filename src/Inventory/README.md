To run the prototype in this state (and in visual studio), you need to:

1. Write "Python" in terminal to use python. (using python console probably works too)
2. While in Python mode, write "from app import db".
3. While in Python mode, wrtie "db.create_all()" to create the database (I believe this is only for sqlite)
4. Exit Python mode and run the app.

To send requests to the server, you need to use curl or any program that can make a request, ex postman.

To get every item in the db you need to call this URL http://127.0.0.1:5000/inventory in GET mode.

To add an item into the db, you need to call this URL http://127.0.0.1:5000/inventory in POST mode with a JSON like this:

Example:
{"item_name" : "Cookie", "item_amount" : "5"}

Cookie is already in the database.
