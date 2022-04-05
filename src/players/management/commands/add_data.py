import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand
import logging, logging.config
from players.models import Player
from sqlalchemy import create_engine



class Command(BaseCommand):
    help = "A command to add data from a csv file to the database."
    """
    def add_arguments(self, parser):
        parser.add_argument(
            "input", type=str, help="Choose directory path with input csv files"
        )
    """

    def handle(self, *args, **options):
        """
        csv_files = self.list_items(options["input"])
        for path in csv_files:
            logging.info(f"Preparing data from {path}...")
            dataframe = self.read_csv(path)
            print(dataframe.head())
        """
        csv_file = "./players/data/2016.csv"
        df = self.read_csv(csv_file)
        print(df.head())
        self.make_sql(df)

    def list_items(self, directory):
        # Directory validation and list matching csv files
        try:
            return sorted([str(item) for item in list(Path(directory).iterdir())])
        except FileNotFoundError:
            raise FileNotFoundError(f"No such file or directory: {directory}")

    def read_csv(self, directory):
        df = pd.read_csv(directory)
        return df

    def make_sql(self, df):
        engine = create_engine("sqlite:///db.db")

        df.to_sql('players_table', if_exists="replace", con=engine, index=True)
