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
    random_grid,
)
from players.exceptions import (
    NoFilesException,
    NotExistingDirectoryException,
)
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import joblib
import time
import multiprocessing as mp
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
            logging.info(f"\nPreparing models from {path}...\n")
            dataframe = self.read_csv(path)

            model_mid = mp.Process(target=self.model_creation(dataframe, "midfielders", MIDFIELD_COLUMNS_FOR_ESTIMATION, midfield_models_list))
            model_att = mp.Process(target=self.model_creation( dataframe, "attackers", ATTACK_COLUMNS_FOR_ESTIMATION, attack_models_list))
            model_def = mp.Process(target=self.model_creation(dataframe, "defenders", DEFEND_COLUMNS_FOR_ESTIMATION, defend_models_list))

            model_mid.start()
            model_att.start()
            model_def.start()
            #model_mid.join()
            #model_att.join()
            #model_def.join()


        max_midfield_model = max(midfield_models_list, key=lambda item: item[1])
        self.save_file(max_midfield_model, output, "midfield")
        
        max_attack_model = max(attack_models_list, key=lambda item: item[1])
        self.save_file(max_attack_model, output, "attack")

        max_defend_model = max(defend_models_list, key=lambda item: item[1])
        self.save_file(max_defend_model, output, "defend")
        
        end = time.time()
        logging.info(f"Operation time: {round((end - start)/60, 2)} min")

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
        X_train, X_test, y_train, y_test = train_test_split(X.values, y)
        rf = RandomForestRegressor()
        model = rf.fit(X_train, y_train.values)
        model_score = rf.score(X_test, y_test.values)
        return (model, model_score)
        
        

    def save_file(self, model, directory, name):
        try:
            joblib.dump(model[0], f"{Path(directory)}/model_{name}.pkl")
            logging.info(f"Prepared new model for {name} players")
            logging.info(f"Best score: {round(model[1], 2)} \n")

        except OSError as e:
            raise NotExistingDirectoryException(
                "Cannot save file into a non-existent directory"
            )


    def model_creation(self, dataframe, position, columns_list, models_list):

        chosen_position = self.position_filter(position, dataframe)
        model = self.model_to_estimate_player_value(chosen_position, columns_list)
        logging.info(f"{position.capitalize()} value estimation model score: {round(model[1], 2)}")
        models_list.append(tuple(model))

