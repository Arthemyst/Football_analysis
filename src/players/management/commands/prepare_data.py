from django.core.management.base import BaseCommand
import pandas as pd
from pathlib import Path
import logging, logging.config
import sys
from players.constants import DEFAULT_COLUMNS
logger = logging.getLogger(__name__)


class MyException(Exception):
    pass

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "input", type=str, help="Choose directory path with input csv files"
        )

        parser.add_argument(
            "output",
            type=str,
            help="Choose directory path when output csv files will save",
        )

    def handle(self, input, output, *args, **options):
        csv_files = self.list_files(input)

        for path in csv_files:
            logging.info(f"Preparing data from {path}...")
            dataframe = self.read_csv(path)
            dataframe = self.remove_goalkeepers(dataframe)
            dataframe = self.optimize_types(dataframe, path)
            self.save_file(dataframe, output, path)

    def list_files(self, directory):
        # Directory validation and list matching csv files
        try:
            return sorted([item for item in Path(directory).iterdir() if item.is_file() and item.name.endswith('csv')])
        except FileNotFoundError as e:
            raise MyException(f"No such file or directory: {directory}") from e

    def read_csv(self, path):
        # Load a csv into a Pandas dataframe and return it
        if not str(path).endswith(".csv"):
            raise MyException(
                f"Not columns to parse from file or not csv format."
            )
        try:
            dataframe = pd.read_csv(
                f"{path}",
                usecols=DEFAULT_COLUMNS,
                index_col=[0],
            )
        except ValueError as e:
            raise e
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
        # save team_position as separated data series
        
        df_name = dataframe["short_name"]
        df_long_name = dataframe["long_name"]
        df_nationality = dataframe["nationality"]
        df_club = dataframe["club"]
        df_position = dataframe["team_position"]
        # drop team_position column for data types optimization
        # dropped columns have object type of data
        # it make problem with optimization of numerical data in othe columns
        # dropped columns will be added in other step
        dataframe.drop(
            [
                "player_positions",
                "team_position",
                "short_name",
                "club",
                "nationality",
                "long_name",
            ],
            axis="columns",
            inplace=True,
        )
        
        # optimizing types of data
        for column in dataframe.columns:
            if dataframe[column].dtypes == "object":
                # in pandas module type "object" is related to string type 
                # remove '+' and '-' from columns with parameters values ex. '65+2'
                # change data type to integer
                dataframe[column] = (
                    dataframe[column].astype(str).apply(lambda x: int(x.split("+")[0]) + int(x.split("+")[1]) if "+" in x else x))               
                dataframe[column] = (
                    dataframe[column].astype(str).apply(lambda x: str(int(x.split("-")[0]) - int(x.split("-")[1])) if "-" in x else x))           
                dataframe[column] = dataframe[column].astype(int)            
            if dataframe[column].dtypes == "float":
                dataframe[column] = dataframe[column].astype(int)

            # add dropped columns to dataframe
        dataframe.insert(0, "short_name", df_name, allow_duplicates=True)
        dataframe.insert(1, "long_name", df_long_name, allow_duplicates=True)
        dataframe.insert(2, "team_position", df_position, allow_duplicates=True)
        dataframe["team_position"] = dataframe["team_position"].astype("category")
        dataframe.insert(3, "club", df_club, allow_duplicates=True)
        # in pandas module type "category" is related to string type 
        dataframe["club"] = dataframe["club"].astype("category")
        dataframe.insert(4, "nationality", df_nationality, allow_duplicates=True)
        dataframe["nationality"] = dataframe["nationality"].astype("category")
        dataframe['year'] = f"20{path.name[8:10]}"
        return dataframe

    def save_file(self, dataframe, directory, path):
        try:
            dataframe.to_csv(f"{Path(directory)}/{path.name}", sep=",", index=False)
            logging.info(
                f"Prepared new csv file: {path.name} for {len(dataframe)} players \n"
            )
        except OSError as e:
            raise MyException(
                f"Cannot save file into a non-existent directory: {directory}"
            )
