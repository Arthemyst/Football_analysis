import logging
import logging.config
from pathlib import Path
from typing import List
import pandas as pd
from django.core.management.base import BaseCommand
from players.constants import (
    MIDFIELD_POSITION_COLUMNS,
    ATTACK_POSITION_COLUMNS,
    DEFEND_POSITION_COLUMNS,
    DEFEND_COLUMNS_FOR_ESTIMATION,
    ATTACK_COLUMNS_FOR_ESTIMATION,
    MIDFIELD_COLUMNS_FOR_ESTIMATION,
)
from players.exceptions import (
    NoFilesException,
    NotExistingDirectoryException,
    WrongFileTypeException,
)
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV
import joblib
import time

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "input", type=str, help="Directory path with input csv files"
        )

        parser.add_argument(
            "output",
            type=str,
            help="Directory path with output estimation models files",
        )

    def handle(self, input, output, *args, **options):
        start = time.time()
        csv_files = self.list_csv_files(input)
        midfield_models_list = []
        attack_models_list = []
        defend_models_list = []
        for path in csv_files:
            logging.info(f"Preparing models from {path}...")
            dataframe = self.read_csv(path)
            midfielders = self.position_filter("midfielders", dataframe)
            model_mid = self.model_to_estimate_player_value(
                midfielders, MIDFIELD_COLUMNS_FOR_ESTIMATION )
            attackers = self.position_filter("attackers", dataframe)
            model_att = self.model_to_estimate_player_value(
                attackers, ATTACK_COLUMNS_FOR_ESTIMATION )
            defenders = self.position_filter("defenders", dataframe)
            model_def = self.model_to_estimate_player_value(
                defenders, DEFEND_COLUMNS_FOR_ESTIMATION )
            logging.info(f"Midfielders value estimation model score: {round(model_mid[1], 2)}")
            logging.info(f"Attackers value estimation model score: {round(model_att[1], 2)}")
            logging.info(f"Defenders calue estimation model score: {round(model_def[1], 2)}")

            midfield_models_list.append(tuple(model_mid))
            attack_models_list.append(tuple(model_att))
            defend_models_list.append(tuple(model_def))


        max_midfield_model = max(midfield_models_list, key=lambda item: item[1])
        self.save_file(max_midfield_model, output)
        max_attack_model = max(attack_models_list, key=lambda item: item[1])
        self.save_file(max_attack_model, output)
        max_defend_model = max(defend_models_list, key=lambda item: item[1])
        self.save_file(max_defend_model, output)
        
        end = time.time()
        logging.info(f"Operation time: {int(end - start)/60} min")

    def list_csv_files(self, directory: str) -> List:
        # Directory validation and list matching csv files
        try:
            return sorted(
                [
                    item
                    for item in Path(directory).iterdir()
                    if item.is_file() and item.name.endswith(".csv")
                ]
            )
        except FileNotFoundError as e:
            raise NoFilesException("No such file or directory") from e

    def read_csv(self, directory):
        df = pd.read_csv(directory)
        return df

    def position_filter(self, position, dataframe):

        if position == "midfielders":
            df = dataframe[dataframe["team_position"].isin(MIDFIELD_POSITION_COLUMNS)]
            df = df[df["value_eur"] != 0]
            return df
        elif position == "attackers":
            df = dataframe[dataframe["team_position"].isin(ATTACK_POSITION_COLUMNS)]
            df = df[df["value_eur"] != 0]
            return df
        elif position == "defenders":
            df = dataframe[dataframe["team_position"].isin(DEFEND_POSITION_COLUMNS)]
            df = df[df["value_eur"] != 0]
            return df
        else:
            print("wrong position")

    def model_to_estimate_player_value(self, dataframe, columns_list):

        X = dataframe[columns_list]
        y = X.pop("value_eur")
        scaler = MinMaxScaler()
        scaler.fit(X)
        scaler.transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        param_grid = [
            {
                "max_depth": [3, 4, 5, 6, 7, 8, 9, 10, 20],
                "min_samples_leaf": [3, 4, 5, 10, 15],
            }
        ]
        gs = GridSearchCV(RandomForestRegressor(), param_grid=param_grid, scoring="r2")
        model = gs.fit(X_train, y_train)
        model_score = gs.score(X_test, y_test)
        return model, model_score

    def save_file(self, model, directory):
        try:
            joblib.dump(model[0], f"{Path(directory)}/model_defend.pkl")
            logging.info(f"Prepared new model for defend players")
            logging.info(f"Best score: {round(model[1], 2)} \n")

        except OSError as e:
            raise NotExistingDirectoryException(
                "Cannot save file into a non-existent directory"
            )
