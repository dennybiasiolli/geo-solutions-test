# Geo Solutions test

## Project initialization

- create a virtualenv using Python 3.8+

    `python3 -m venv venv`

- activate the virtualenv

    `source venv/bin/activate`

- install requirements

    - `pip install -r requirements.txt` for production usage

    - `pip install -r requirements_dev.txt` for development


## Project execution

```sh
# creating django settings file from dev
cp src/website/settings_dev.py src/website/settings.py
# creating/migrating database
python src/manage.py migrate
# creating default users
python src/manage.py geo_create_users
# importing coordinaates
python src/manage.py geo_import_coordinates_from_csv -f data/points.csv
# running server
python src/manage.py runserver
```


## Request

You shall create a simple application Django 2.2+ / Python 3.6+ which,
upon login, exposes a simple interface where the user can execute one or more
requests according to these characteristics:

Storage:
- A list of x, y coordinates representing geospatial points
    (see CSV [here](data/points.csv))

- The DB must be populated through an ad hoc management command

- Two Django users (us: user1/user2, pw: user1/user2) will be pre-registered 

- A dedicated table will store the results (see below) for each user


Inputs:

- `<x:float>` X coordinate

- `<y:float>` Y coordinate

- `<n:int>` number of points to be returned

- `<operation:type>` nearest, furthest


Outputs:

- The backend will calculate, asynchronously, the first N points closest to
    or farthest, depending on the selected operation, to the coordinates
    entered by the user.


Requirements:

- REST API under Basic Auth with:

    - Endpoint to perform a request

    - Endpoint to retrieve the history of results


Tests:

- Mandatory for the API

Delivery:

- The code must be shared through a Pull Request made on a GitHub repository
    specially created by you, from the "exercise" branch to the "master" branch.
