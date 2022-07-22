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
            "output", type=str, help="Directory path with output estimation models files"
        )

    def handle(self, input, output, *args, **options):
        csv_files = self.list_csv_files(input)

        for path in csv_files:
            logging.info(f"Preparing models from {path}...")
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

    def read_csv(self, directory):
        df = pd.read_csv(directory)
        return df
def columns_for_estimation(dataframe, position):
    if position == "attacker":
        columns = columns_attacker
    elif position == "defender":
        columns = columns_defender
    elif position == "midfielder":
        columns = columns_midfielder

    dataframe = dataframe[dataframe['value_eur'] != 0]
    corr = dataframe[columns].corr()
    best_corr = corr[corr['value_eur'] > 0.4]
    columns_for_estimation = [column for column in best_corr.index]

    return columns_for_estimation