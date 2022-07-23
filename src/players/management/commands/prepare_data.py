import logging
import logging.config
from pathlib import Path
from typing import List

import pandas as pd
from django.core.management.base import BaseCommand

from players.constants import (DEFAULT_COLUMNS, UNOPTIMIZABLE_COLUMNS,
                               VALUES_COLUMNS)
from players.exceptions import (NoFilesException,
                                NotExistingDirectoryException,
                                WrongFileTypeException)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "input", type=str, help="Directory path with input csv files"
        )

        parser.add_argument(
            "output", type=str, help="Directory path with output csv files"
        )

    def handle(self, input, output, *args, **options):
        csv_files = self.list_csv_files(input)

        for path in csv_files:
            logging.info(f"Preparing data from {path}...")
            dataframe = self.read_csv(path)
            dataframe = self.remove_goalkeepers(dataframe)
            dataframe = self.optimize_types(dataframe, path)
            self.save_file(dataframe, output, path)

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

    def read_csv(self, path):
        # Load a csv into a Pandas dataframe and return it
        dataframe = pd.read_csv(f"{path}", usecols=DEFAULT_COLUMNS, index_col=[0])

        return dataframe

    def remove_goalkeepers(self, dataframe):
        # remove goalkeepers from dataframe
        # goalkeepers have different parameters and is not able to compare it with field players
        dataframe.reset_index(inplace=True)
        dataframe = dataframe[dataframe["team_position"] != "SUB"]
        dataframe = dataframe[dataframe["team_position"] != "RES"]
        dataframe = dataframe[dataframe["player_positions"] != "GK"]
        dataframe.dropna(subset=["team_position"], inplace=True)
        return dataframe

    def optimize_types(self, dataframe, path):
        def sum_values(value: str) -> int:
            """remove '+' and '-' from columns with parameters values ex. '65+2'
            change data type to integer"""
            if "+" in value:
                return int(value.split("+")[0]) + int(value.split("+")[1])
            elif "-" in value:
                return int(value.split("-")[0]) - int(value.split("-")[1])
            else:
                return int(value)

        # optimizing types of data
        for column in dataframe.columns:
            if column in UNOPTIMIZABLE_COLUMNS:
                continue
            elif dataframe[column].dtypes == "object":
                # in pandas module type "object" is related to string type
                dataframe[column] = dataframe[column].astype(str).apply(sum_values)
            elif dataframe[column].dtypes == "float":
                dataframe[column] = dataframe[column].astype(int)

        dataframe["team_position"] = dataframe["team_position"].astype("category")
        # in pandas module type "category" is related to string type
        dataframe["nationality"] = dataframe["nationality"].astype("category")
        dataframe["year"] = f"20{path.name[8:10]}"
        dataframe = dataframe[~(dataframe[VALUES_COLUMNS] < 0).any(axis=1)]
        dataframe["club"] = dataframe["club"].str.replace("1. ", "", regex=True)
        dataframe["club"] = dataframe["club"].astype("category")

        return dataframe

    def save_file(self, dataframe, directory, path):
        try:
            dataframe.to_csv(f"{Path(directory)}/{path.name}", sep=",", index=False)
            logging.info(
                f"Prepared new csv file: {path.name} for {len(dataframe)} players \n"
            )
        except OSError as e:
            raise NotExistingDirectoryException(
                "Cannot save file into a non-existent directory"
            )
