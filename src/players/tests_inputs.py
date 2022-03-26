# file to create csv files with dataframe to test modules from prepare_data menagement command
# dataframes obtains only 5 first rows from original dataframes

import pandas as pd
from pathlib import Path
import sys
from constants import DEFAULT_COLUMNS

cwd = Path.cwd()

# prepare test dataframe
# to check read_csv module from prepare_data management command

reader = pd.read_csv(
    f"{cwd}/src/players/input_data/players_16.csv",
    usecols=DEFAULT_COLUMNS,
    index_col=[0],
)

reader_head = reader.head()
reader_head.to_csv(f"{cwd}/src/players/tests_inputs/reader.csv", index=False)

# prepare test dataframe to check remove_goalkeepers module

remove_gk = reader.copy()
# remove_gk.reset_index(inplace=True)
# remove_gh = remove_gk.pop()
remove_gk = remove_gk[remove_gk["team_position"] != "SUB"]
remove_gk = remove_gk[remove_gk["team_position"] != "RES"]
remove_gk = remove_gk[remove_gk["player_positions"] != "GK"]
remove_gk.dropna(subset=["team_position"], inplace=True)
remove_gk_head = remove_gk.head()
remove_gk_head.to_csv(f"{cwd}/src/players/tests_inputs/remove_gk.csv")

# prepare test optimize to check optimize_types module
optimize = remove_gk.copy()
optimize.reset_index(inplace=True)
# save team_position as separated data series
df_name = optimize["short_name"]

df_long_name = optimize["long_name"]
df_nationality = optimize["nationality"]
df_club = optimize["club"]
df_position = optimize["team_position"]
# drop team_position column for data types optimization
# dropped columns have object type of data
# it make problem with optimization of numerical data in othe columns
# dropped columns will be added in other step
optimize.drop(
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
for column in optimize.columns:
    # optimize.rename({column: f"{column}_{path[8:10]}"})
    if optimize[column].dtypes == "object":
        # remove '+' and '-' from columns with parameters values ex. '65+2'
        optimize[column] = (
            optimize[column].astype("object").apply(lambda x: x.split("+")[0])
        )
        optimize[column] = (
            optimize[column].astype("object").apply(lambda x: x.split("-")[0])
        )
        # change data type to integer
        optimize[column] = optimize[column].astype(int)
    else:
        optimize[column] = optimize[column].astype(int)

    # add dropped columns to optimize
    optimize["team_position"] = df_position
    optimize["team_position"] = optimize["team_position"].astype("category")
    optimize["club"] = df_club
    optimize["club"] = optimize["club"].astype("category")
    optimize["nationality"] = df_nationality
    optimize["nationality"] = optimize["nationality"].astype("category")
    optimize["short name"] = df_name
    optimize["long_name"] = df_long_name
# optimize.drop(optimize.columns[0], axis=1, inplace=True)
optimize_head = optimize.head()
optimize_head.to_csv(f"{cwd}/src/players/tests_inputs/optimize_types.csv", index=False)
