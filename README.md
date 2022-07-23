# Football-analysis

## Introduction

Program will be used to vizualization data about football players.
Data of players are uploaded from FIFA databases prepared by member of kaggle.com community: https://www.kaggle.com/stefanoleone992/fifa-20-complete-player-dataset
Databases are separated by years, from 2016 to 2020. In program we can look how parameters are related to player overall rate and player value. We can compare players parameters, make visualisation of clubs, positions, nationality rankings etc.
Data vizualization is based on python libraries like pandas, plotly, nupmy.
Vizualization works with website with usage of Django framework.

Features:
- compare players parameters
- find players in club and filter by year
- find detail of player in list of all players
- find player in search field
- estimate player value by choosing specific parameters related to position on field (midfielder, attacker, defender)

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Arthemyst/Football_analysis.git
$ cd Football_analysis
```

This project requires Python 3.6 or later.

Create a virtual environment to install dependencies in and activate it:

Linux:
```sh
$ python3 -m venv env
$ source env/bin/activate
```

Create a .env file in project root directory. The file format can be understood from the example below:
```sh
DEBUG=True
SECRET_KEY=your-secret-key # generate your own secret key
DATABASE_URL=psql://postgres:postgres@database:5432/postgres
ALLOWED_HOSTS=127.0.0.1,localhost
```
Application runs on docker. Please run docker-compose to install dependiences and run application:
```sh
$ docker-compose -f docker/docker-compose.yaml up --build
```

To test management commands during application running:
```sh
(env)$ docker exec -it docker_web_1 /bin/bash
(env)$ python3 -m pytest players/tests/tests_prepare_data.py
(env)$ python3 -m pytest players/tests/tests_add_data.py
```

To transform data from inpu csv files:
Warning: need to download data from https://www.kaggle.com/stefanoleone992/fifa-20-complete-player-dataset and create directory in players/ named "input_data".
```sh
(env)$ docker exec -it docker_web_1 /bin/bash
(env)$ python3 manage.py prepare_data players/input_data players/data
```

To load data to database:
```sh
(env)$ docker exec -it docker_web_1 /bin/bash
(env)$ python3 manage.py add_data players/data
```

