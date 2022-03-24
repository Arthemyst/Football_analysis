from django.core.management.base import BaseCommand
import pandas as pd
from pathlib import Path
import logging, logging.config
import sys
from players.constants import DEFAULT_COLUMNS

# Django Logging Information
LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        }
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}
logging.config.dictConfig(LOGGING)


class Command(BaseCommand):
    help = "Displays stats related to Article and Comment models"

    def add_arguments(self, parser):
        parser.add_argument(
            "input", type=str, help="Choose directory path with input csv files"
        )

        parser.add_argument(
            "output",
            type=str,
            help="Choose directory path when output csv files will save",
        )

    def handle(self, *args, **options):
        csv_files = self.list_items(options["input"])
        df_list = []
        for path in csv_files:
            logging.info(f"Preparing data from {path}...")
            dataframe = self.read_csv(path)

            dataframe = self.remove_goalkeepers(dataframe)

            dataframe = self.optimize_types(dataframe)

            # add dataframe to list
            df_list.append(dataframe)

        for dataframe, name in zip(df_list, csv_files):

            self.save_file(dataframe, options["output"], name)

    def list_items(self, directory):
        # Directory validation and list matching csv files
        try:
            return sorted([str(item) for item in list(Path(directory).iterdir())])
        except:
            raise FileNotFoundError(f"No such file or directory: {directory}")

    def read_csv(self, path):
        # Load a csv into a Pandas dataframe and return it
        dataframe = pd.read_csv(
            f"{path}",
            usecols=DEFAULT_COLUMNS,
            index_col=[0],
        )
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

    def optimize_types(self, dataframe):
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
            # dataframe.rename({column: f"{column}_{path[8:10]}"})
            if dataframe[column].dtypes == "object":
                # remove '+' and '-' from columns with parameters values ex. '65+2'
                dataframe[column] = (
                    dataframe[column].astype("object").apply(lambda x: x.split("+")[0])
                )
                dataframe[column] = (
                    dataframe[column].astype("object").apply(lambda x: x.split("-")[0])
                )
                # change data type to integer
                dataframe[column] = dataframe[column].astype(int)
            else:
                dataframe[column] = dataframe[column].astype(int)

            # add dropped columns to dataframe
            dataframe["team_position"] = df_position
            dataframe["team_position"] = dataframe["team_position"].astype("category")
            dataframe["club"] = df_club
            dataframe["club"] = dataframe["club"].astype("category")
            dataframe["nationality"] = df_nationality
            dataframe["nationality"] = dataframe["nationality"].astype("category")
            dataframe["short name"] = df_name
            dataframe["long_name"] = df_long_name
        return dataframe

    def save_file(self, dataframe, directory, name):
        try:
            dataframe.to_csv(f"{Path(directory)}/20{name[-6::]}", sep=",", index=False)
            logging.info(
                f"Prepared new csv file: 20{name[-6::]} for {len(dataframe)} players"
            )
        except:
            raise OSError(
                f"Cannot save file into a non-existent directory: {directory}"
            )
