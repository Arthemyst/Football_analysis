# Football-analysis

## Introduction

The program will be used to visualize data about football players
Players data are collected from FIFA databases prepared by a member of the kaggle.com community: https://www.kaggle.com/stefanoleone992/fifa-20-complete-player-dataset
Databases are separated by years, from 2016 to 2020.

Process of preparing data:
1. Extract data from cvs files,
2. Transform data - automated in prepare_data management command,
3. Upload data to the postgresql database - automated in add_data management command,
4. Create players value estimation models separated by positions (midfielders, attackers, defenders) - automated in prepare_value_estimation_models management command.

In program we can look how parameters was changing during years. We can compare players parameters, make visualisation of clubs, positions, nationality.
Data vizualization is based on python libraries like pandas, plotly, nupmy.
Estimation models are based on scikit-learn library and the Random Forest Regressor used.
Vizualization of website is based on Django framework.

Features:
- compare players parameters
- find players in club and filter these by year
- find detail of player
- find player in dedicated search field
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
(env)$ python3 -m pytest players/tests/tests_prepare_estimation_models.py

```

To transform data from input csv files:
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
To prepare players value estimation models:
```sh
(env)$ docker exec -it docker_web_1 /bin/bash
(env)$ python3 manage.py prepare_estimation_models players/data players/models
```
