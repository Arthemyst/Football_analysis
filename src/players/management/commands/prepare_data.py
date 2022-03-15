from django.core.management.base import BaseCommand
import pandas as pd
from pathlib import Path
from os import listdir
from os.path import isfile, join
from functools import reduce
import logging, logging.config
import sys

# Django Logging Information
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
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
        
        
        basepath = options["input"]
        csv_list = sorted([item for item in listdir(basepath)])
        df_list = list()

        for df_csv in csv_list:
            logging.info(f'Preparing data from {df_csv}...')
            df_field_players = pd.read_csv(
                f"{basepath}/{df_csv}",
                usecols=[
                    "short_name",
                    "long_name",
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
                index_col=[0],
            )
            df_field_players.reset_index(inplace=True)
            df_field_players = df_field_players[
                df_field_players["team_position"] != "SUB"
            ]
            df_field_players.dropna(subset=["team_position"], inplace=True)
            df_field_players = df_field_players[
                df_field_players["team_position"] != "RES"
            ]
            df_field_players = df_field_players[
                df_field_players["player_positions"] != "GK"
            ]
            # save team_position as separated data series
            df_name = df_field_players["short_name"]
            df_long_name = df_field_players["long_name"]
            df_nationality = df_field_players["nationality"]
            df_club = df_field_players["club"]
            df_position = df_field_players["team_position"]
            # drop team_position column for data types optimization
            df_field_players.drop(
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
            for column in df_field_players.columns:
                df_field_players.rename({column: f"{column}_{df_csv[8:10]}"})
                if df_field_players[column].dtypes == "object":
                    # remove '+' and '-' from columns with parameters values ex. '65+2'
                    df_field_players[column] = (
                        df_field_players[column]
                        .astype("object")
                        .apply(lambda x: x.split("+")[0])
                    )
                    df_field_players[column] = (
                        df_field_players[column]
                        .astype("object")
                        .apply(lambda x: x.split("-")[0])
                    )
                    # change data type for integer
                    df_field_players[column] = df_field_players[column].astype(int)
                else:
                    df_field_players[column] = df_field_players[column].astype(int)

                # change player value for millions of euro
                """
                df_field_players.loc[:, "value_eur"] *= 0.000001
                df_field_players.rename(
                    columns={"value_eur": "value_eur_mln"}, inplace=True
                )
                """
                # add again team_position column to dataframe
                df_field_players["team_position"] = df_position
                df_field_players["team_position"] = df_field_players[
                    "team_position"
                ].astype("category")
                df_field_players["club"] = df_club
                df_field_players["club"] = df_field_players["club"].astype("category")
                df_field_players["nationality"] = df_nationality
                df_field_players["nationality"] = df_field_players[
                    "nationality"
                ].astype("category")
                df_field_players["short name"] = df_name
                df_field_players["long_name"] = df_long_name
                # df_field_players.reset_index(inplace=True)
                # df_field_players.reset_index(inplace=True)
                
            df_list.append(df_field_players)

        for df, name in zip(df_list, csv_list):
            
            logging.info(f'Prepared new csv file: 20{name[-6::]} for {len(df)} players')
            for col in df.columns:
                df.rename(columns={col: f"{col}_{name[8:10]}"}, inplace=True)
            df.rename(columns={df.columns[-2]: "short_name"}, inplace=True)
            df.rename(columns={df.columns[-1]: "long_name"}, inplace=True)
            df.rename(columns={df.columns[-3]: "nationality"}, inplace=True)
            df.to_csv(f"{options['output']}20{name[-6::]}", sep=",", index=False)

        
        
        