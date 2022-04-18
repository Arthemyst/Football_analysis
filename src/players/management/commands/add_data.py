import logging
import logging.config
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine

from players.constants import (DEFAULT_COLUMNS, UNOPTIMIZABLE_COLUMNS,
                               VALUES_COLUMNS)
from players.exceptions import (NoFilesException,
                                NotExistingDirectoryException,
                                WrongFileTypeException)
from players.models import Player, PlayerStatistics


class Command(BaseCommand):
    help = "A command to add data from a csv file to the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "input", type=str, help="Choose directory path with input csv files"
        )

    def handle(self, *args, **options):

        csv_files = self.list_csv_items(options["input"])

        for path in csv_files:
            logging.info(f"Preparing data from {path}...")
            dataframe = self.read_csv(path)

            # csv_file = "./players/data/players_16.csv"
            df = self.read_csv(path)
            self.make_sql(df)

    def list_csv_items(self, directory):
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

    def make_sql(self, df):
        for _, row in df.iterrows():
            Player.objects.get_or_create(
                short_name=row["short_name"],
                long_name=row["long_name"],
                nationality=row["nationality"],
            )
            player = Player.objects.get(
                short_name=row["short_name"],
                long_name=row["long_name"],
                nationality=row["nationality"],
            )
            player.save()
            PlayerStatistics.objects.get_or_create(
                player=player,
                year=row["year"],
                team_position=row["team_position"],
                club=row["club"],
                age=row["age"],
                overall=row["overall"],
                value_eur=row["value_eur"],
                pace=row["pace"],
                shooting=row["shooting"],
                passing=row["passing"],
                dribbling=row["dribbling"],
                defending=row["defending"],
                physic=row["physic"],
                attacking_crossing=row["attacking_crossing"],
                attacking_finishing=row["attacking_finishing"],
                attacking_heading_accuracy=row["attacking_heading_accuracy"],
                attacking_short_passing=row["attacking_short_passing"],
                attacking_volleys=row["attacking_volleys"],
                skill_dribbling=row["skill_dribbling"],
                skill_curve=row["skill_curve"],
                skill_fk_accuracy=row["skill_fk_accuracy"],
                skill_long_passing=row["skill_long_passing"],
                skill_ball_control=row["skill_ball_control"],
                movement_acceleration=row["movement_acceleration"],
                movement_sprint_speed=row["movement_sprint_speed"],
                movement_agility=row["movement_agility"],
                movement_reactions=row["movement_reactions"],
                movement_balance=row["movement_balance"],
                power_shot_power=row["power_shot_power"],
                power_jumping=row["power_jumping"],
                power_stamina=row["power_stamina"],
                power_strength=row["power_strength"],
                power_long_shots=row["power_long_shots"],
                mentality_aggression=row["mentality_aggression"],
                mentality_interceptions=row["mentality_interceptions"],
                mentality_positioning=row["mentality_positioning"],
                mentality_vision=row["mentality_vision"],
                mentality_penalties=row["mentality_penalties"],
                defending_marking=row["defending_marking"],
                defending_standing_tackle=row["defending_standing_tackle"],
                defending_sliding_tackle=row["defending_sliding_tackle"],
            )
        """
        engine = create_engine("postgresql://postgres:postgres@127.0.0.1:5432/postgres")

        df.to_sql(Player, if_exists="replace", con=engine, index=True)
        """
