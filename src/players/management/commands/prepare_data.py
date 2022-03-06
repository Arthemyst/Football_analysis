from django.core.management.base import BaseCommand
import pandas as pd
from pathlib import Path
from os import listdir
from os.path import isfile, join


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

    def handle(self, *args, **kwargs):
        basepath = Path("input")
        input_files = [f for f in listdir(basepath) if isfile(join(basepath, f))]
        csv_list = [item for item in listdir(basepath) if item.is_file]
        df_list = list()

        for df_csv in csv_list:
            df_field_players = pd.read_csv(
                f"data_input/{df_csv}",
                usecols=[
                    "short_name",
                    "nationality",
                    "club",
                    "age",
                    "attacking_crossing",
                    "attacking_finishing",
                    "attacking_heading_accuracy",
                    "attacking_short_passing",
                    "attacking_volleys",
                    "defending",
                    "defending_marking",
                    "defending_sliding_tackle",
                    "defending_standing_tackle",
                    "dribbling",
                    "mentality_aggression",
                    "mentality_interceptions",
                    "mentality_penalties",
                    "mentality_positioning",
                    "mentality_vision",
                    "movement_acceleration",
                    "movement_agility",
                    "movement_balance",
                    "movement_reactions",
                    "movement_sprint_speed",
                    "pace",
                    "passing",
                    "physic",
                    "power_jumping",
                    "power_long_shots",
                    "power_shot_power",
                    "power_stamina",
                    "power_strength",
                    "shooting",
                    "skill_ball_control",
                    "skill_curve",
                    "skill_dribbling",
                    "skill_fk_accuracy",
                    "skill_long_passing",
                    "team_position",
                    "player_positions",
                    "overall",
                    "value_eur",
                ],
            )
            df_list.append(df_field_players)

        for df, name in zip(df_list, input_files):

            df.to_csv(f"{'output'}20{name[-6::]}", sep=",")
