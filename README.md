![Logo of the project](https://github.com/DAT210/conventions/blob/master/images/modules.png)

# Logistics &middot; [![Build Status](https://img.shields.io/travis/npm/npm/latest.svg?style=flat-square)](https://travis-ci.org/npm/npm) [![npm](https://img.shields.io/npm/v/npm.svg?style=flat-square)](https://www.npmjs.com/package/npm) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/your/your-project/blob/master/LICENSE)

Logistics, made by Group 5, handles the inventory database.

## Installing / Getting started

The API can be run on docker, currently tested only on docker-toolbox, and local on the machine, which requires MySQL, Python and packages shown in requirements.txt.

```shell
git clone https://github.com/DAT210/Logistics
```

This will clone the project into your computer.

### Initial configuration

```shell
Run setup.py
```

Use python shell and run the setup script located in the tools folder to create the SSL certification.

```shell
Create .env file in the root of the project and add:
  DB_USERNAME=<username>
  DB_PASS=<password>
  ROOT_PASS=<password>
  SECRET_KEY=<secret>
```

This will create a .env file which docker and the program will read from, replace the brackets with the username you want to login with to the database, the corresponding password to the user, the root password for the database and last the secret key which you can use any string, reccomended to create a random string.

### !!! Currenly you need to add these lines into the .env file !!!

```shell
JWT_USER=<username>
JWT_PASS=<password>
```

This will create a login profile to use JWT.

To connect to the API, use https://192.168.99.100:5501/ for docker toolbox or https://127.0.0.1:5501/ for docker

## Developing

### Built With
Python 3.3.6
Flask 1.0.2
Sqlalchemy 1.2.12
Flask-sqlalchemy 2.3.1
Pyjwt 1.6.4
Pymysql 0.9.2
Pyopenssl 18.0.0


### Prerequisites
[MySQL](https://www.mysql.com/downloads/)

[Pyton](https://www.python.org/downloads/)

[Docker](https://www.docker.com/products/docker-desktop)

pip install Flask

pip install Sqlalchemy

pip install flask-sqlalchemy

pip install pyjwt

pip install pymysql

pip install pyopenssl



### Setting up Dev

```shell
git clone https://github.com/your/your-project.git
cd your-project/
install the prerequisites
create .env file and add:
  INV_JWT_USER=<username>
  INV_JWT_PASS=<password>
  DB_USERNAME=<username>
  DB_PASS=<password>
  ROOT_PASS=<password>
  SECRET_KEY=<secret>
PYTHON runDev.py
```

The parameters in the .env file will be read by the program, and these two will override the login information to use jwt tokens. Then with python run the runDev script to start the server in development mode, which will enable debug, set ip address to 127.0.0.1:5000 and a simple secret key.

## Versioning

We can maybe use [SemVer](http://semver.org/) for versioning. For the versions available, see the [link to tags on this repository](/tags).


## Tests

To run the tests, simply run the test_ingredients.py and test_locations.py, which will create a temporary database. These tests will test the wanted functionality of the API, to see if the functionality works. These tests will also test some errorhandlers.

```shell
def test_get_all_locations(self):
        response = self.app.get('v1/locations/', headers=self.headers)
        self.assertEqual('200 OK', response.status)
```

## Style guide

Explain your code style and show how to check it.

## Api Reference

If the api is external, link to api documentation. If not describe your api including authentication methods as well as explaining all the endpoints with their required parameters.

### Login

```shell
GET     /v1/locations/login
SEND    Basic Auth Login
RECIEVE {
            "token": <token>
        }
```

### GET all

```shell
GET     /v1/locations/
SEND    
CODE    200
RECIEVE {
        "locations": [
        {
            "id": <id>,
            "name": <name>
        },
        {
            "id": <id>,
            "name": <name>
        }]
}
```

```shell
GET     /v1/locations/<id>/ingredients
SEND
CODE    200
RECIEVE {
        "ingredients": [
        {
            "amount": <amount>,
            "name": <name>
        },
        {
            "amount": <amount>,
            "name": <name>
        }]
}
```

### GET one

```shell
GET     /v1/locations/<id>
SEND    
CODE    200
RECIEVE {
          "id": <id>,
          "name": <name>
}
```

```shell
GET     /v1/locations/<id>/ingredients/<name>
SEND    
CODE    200
RECIEVE {
          "amount": <amount>,
          "name": <name>
}
```

### POST

```shell
POST     /v1/locations/
SEND    {
          "locationName": <name>
}
RECIEVE {
          "code": 201,
          "message": <message>,
          "description": <description>
}
```

```shell
POST     /v1/locations/<id>/ingredients
SEND    {
          "ingredientName": <name>,
          "ingredientAmount": <amount>
}  
RECIEVE {
          "code": 201,
          "message": <message>,
          "description": <description>
}
```

### PUT

```shell
PUT     /v1/locations/<id>
SEND    {
          "locationName": <name>
}
RECIEVE {
          "code": 204,
          "message": <message>,
          "description": <description>
}
```

```shell
PUT     /v1/locations/<id>/ingredients/<name>
SEND    {
          "ingredientAmount": <amount>
}  
RECIEVE {
          "code": 204,
          "message": <message>,
          "description": <description>
}
```

### DELETE

```shell
DELETE     /v1/locations/<id>
SEND    
RECIEVE {
          "code": 204,
          "message": <message>,
          "description": <description>
}
```

```shell
DELETE     /v1/locations/<id>/ingredients/<name>
SEND    
RECIEVE {
          "code": 204,
          "message": <message>,
          "description": <description>
}
```

## Database

Explaining what database (and version) has been used. Provide download links.
Documents your database design and schemas, relations etc... 

## Licensing

State what the license is and how to find the text version of the license.
