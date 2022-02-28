# Football-analysis

## Introduction

Program will be used to vizualization data about football players.
Data of players are uploaded from FIFA databases prepared by member of kaggle.com community: https://www.kaggle.com/stefanoleone992/fifa-20-complete-player-dataset
Databases are separated by years, from 2016 to 2020. In program we can look how parameters are related to player overall rate and player value. We can compare players parameters, make visualisation of clubs, positions, nationality rankings etc.
Data vizualization is based on python libraries like pandas, matplotlib, nupmy.
Vizualization works with website with usage of Django framework.

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Arthemyst/Football_analysis.git
$ cd Football_analysis
```

Create a virtual environment to install dependencies in and activate it:

Linux:
```sh
$ python3 -m venv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```


Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd src
(env)$ python3 manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.
