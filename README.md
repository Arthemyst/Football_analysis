# Football-analysis

## Introduction

The program will be used to visualize data about football players. 
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

## Images from website

Home page before logging
![home](https://user-images.githubusercontent.com/59807704/180871565-3b0e32b4-247c-4477-a9da-93d00c733e13.png)

Home page after logging
![home_after_log](https://user-images.githubusercontent.com/59807704/180871959-8c1d1460-a4af-4cbc-b5cc-1ce2d6ada500.png)

Page with players list
![players_list](https://user-images.githubusercontent.com/59807704/180872045-0497ffae-3910-4aef-b15d-1d9e9476fbe9.png)

Page with details of chosen player
![player_detail](https://user-images.githubusercontent.com/59807704/180872320-25414485-3461-44af-8d40-70b27d8f9c68.png)

Page for searching club
![club_search](https://user-images.githubusercontent.com/59807704/180872401-d0be0544-2e38-4acf-8709-0047ae267f54.png)

Page with searched club
![club_searched](https://user-images.githubusercontent.com/59807704/180872500-4189fc4b-a127-495e-8f67-4c5d0daa7b7a.png)

Page with players comparison
![compare](https://user-images.githubusercontent.com/59807704/180872629-8b1b26f2-c9ca-4f78-ae46-ec193b1b1450.png)

Page for player value estimation
![estimat](https://user-images.githubusercontent.com/59807704/180872835-73fe3912-2a0b-4759-b89e-af274b8f71ee.png)

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
$ python3 -m venv venv
$ source venv/bin/activate
```

Windows:
```sh
$ python3 -m venv venv
$ source venv\Scripts\activate
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

Please first create superuser and migrate database:
```sh
(env)$ docker exec -it docker_web_1 /bin/bash
(env)$ python3 manage.py createsuperuser
(env)$ python3 manage.py migrate
(env)$ python3 manage.py makemigrations
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
