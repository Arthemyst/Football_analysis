import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

cwd = Path.cwd()

df16 = pd.read_csv(f"{cwd}/src/players/data/2016.csv")
df17 = pd.read_csv(f"{cwd}/src/players/data/2017.csv")
df18 = pd.read_csv(f"{cwd}/src/players/data/2018.csv")
df19 = pd.read_csv(f"{cwd}/src/players/data/2019.csv")
df20 = pd.read_csv(f"{cwd}/src/players/data/2020.csv")


def nationality(nationality, df):
    return df[df["nationality"] == nationality]


def prepare_graph(df, y_axis, x_axis, year, x_axis_name, y_axis_name):
    if not isinstance(x_axis, str):
        raise TypeError("Please set x_axis as string.")
    if not isinstance(y_axis, str):
        raise TypeError("Please set y_axis as string.")
    if not isinstance(y_axis_name, str):
        raise TypeError("Please set y_axis_name as string.")
    if not isinstance(y_axis_name, str):
        raise TypeError("Please set y_axis_name as string.")
    sns.set_theme(style="darkgrid")
    f, ax = plt.subplots(figsize=(6.5, 6.5))
    sns.scatterplot(
        x=x_axis,
        y=y_axis,
        palette="ch:r=-.2,d=.3_r",
        sizes=(1, 8),
        linewidth=0,
        data=df,
        ax=ax,
    )
    # plt.scatter(x=df[x_axis], y=df[y_axis])

    if x_axis_name == None:
        plt.xlabel(x_axis)
        plt.ylabel(y_axis_name)
    elif y_axis_name == None:
        plt.xlabel(x_axis_name)
        plt.ylabel(y_axis)
    elif y_axis_name == None and x_axis_name == None:
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
    else:
        plt.xlabel(x_axis_name)
        plt.ylabel(y_axis_name)

    plt.savefig(f"{cwd}/src/players/graphs/{x_axis}_{y_axis}_{year}.png")
    plt.close()
    print(f"graph prepared as: {x_axis}_{y_axis}_{year}.png")


def players_by_position(df, position):
    """Function to select players by position on field: defence, midfield or
    attack.
    """

    if position == "defence":
        defence = df["team_position"].isin(
            ["LWB", "RWB", "CB", "RB", "LB", "RCB", "LCB"]
        )
        data = df.loc[defence]
        data = data[
            [
                "attacking_heading_accuracy",
                "attacking_short_passing",
                "defending",
                "defending_marking",
                "defending_sliding_tackle",
                "defending_standing_tackle",
                "mentality_interceptions",
                "movement_reactions",
                "skill_ball_control",
                "skill_long_passing",
                "value_eur_mln",
                "overall",
                "age",
            ]
        ]

    elif position == "midfield":
        midfield = df["team_position"].isin(
            ["LAM", "CM", "RAM", "RDM", "LM", "LCM", "RM", "LDM", "CDM", "RCM", "CAM"]
        )
        data = df.loc[midfield]
        data = data[
            [
                "attacking_crossing",
                "attacking_finishing",
                "attacking_short_passing",
                "attacking_volleys",
                "dribbling",
                "mentality_positioning",
                "mentality_vision",
                "movement_reactions",
                "passing",
                "power_long_shots",
                "power_shot_power",
                "shooting",
                "skill_ball_control",
                "skill_curve",
                "skill_dribbling",
                "skill_long_passing",
                "value_eur",
                "overall",
                "age",
            ]
        ]

    elif position == "attack":
        attack = df["team_position"].isin(
            ["LF", "RF", "RS", "LS", "CF", "ST", "LW", "RW"]
        )
        data = df.loc[attack]
        data = data[
            [
                "attacking_crossing",
                "attacking_finishing",
                "attacking_short_passing",
                "attacking_volleys",
                "dribbling",
                "mentality_positioning",
                "mentality_vision",
                "movement_reactions",
                "passing",
                "power_long_shots",
                "power_shot_power",
                "shooting",
                "skill_ball_control",
                "skill_curve",
                "skill_dribbling",
                "skill_fk_accuracy",
                "overall",
                "value_eur_mln",
                "age",
            ]
        ]
    else:
        raise ValueError("Please choose 'defence', 'midfield' or 'attack'")

    return data


england = nationality("England", df16)
# england.loc[:, "value_eur"] *= 0.000001
# england["value_eur"] = england["value_eur"].apply(lambda x: x * 0.000001)
# england = england.rename(columns={"value_eur": "value_eur_mln"})

midfielders = players_by_position(df16, "midfield")

prepare_graph(
    df=midfielders,
    y_axis="age",
    x_axis="overall",
    year=2016,
    y_axis_name="Age of midfield players",
    x_axis_name="Overall rating",
)
prepare_graph(
    df=england,
    y_axis="pace",
    x_axis="overall",
    year=2016,
    y_axis_name="Pace of player",
    x_axis_name="Overall rating",
)

prepare_graph(
    df=midfielders,
    y_axis="value_eur",
    x_axis="overall",
    year=2016,
    y_axis_name="Value of midfield player",
    x_axis_name="Overall rating",
)

prepare_graph(
    df=midfielders,
    y_axis="value_eur",
    x_axis="passing",
    year=2016,
    y_axis_name="Value of player",
    x_axis_name="Physic parameter",
)
