from re import M
import pandas as pd
from functools import reduce

df15 = pd.read_csv("/home/pawel/Football_analysis/src/players/data/2015.csv")
df16 = pd.read_csv("/home/pawel/Football_analysis/src/players/data/2016.csv")
df17 = pd.read_csv("/home/pawel/Football_analysis/src/players/data/2017.csv")
df18 = pd.read_csv("/home/pawel/Football_analysis/src/players/data/2018.csv")
df19 = pd.read_csv("/home/pawel/Football_analysis/src/players/data/2019.csv")
df20 = pd.read_csv("/home/pawel/Football_analysis/src/players/data/2020.csv")

df_list = [df19, df20]
merged_df = reduce(
    lambda l, r: pd.merge(
        l, r, on=["short_name", "long_name", "nationality"], how="inner"
    ),
    df_list,
)
print(f"Merge: {len(merged_df)}")
merged_df.drop_duplicates(inplace=True)
print(f"15: {len(df15)}")
print(f"16: {len(df16)}")
print(f"17: {len(df17)}")
print(f"18: {len(df18)}")
print(f"19: {len(df19)}")
print(f"20: {len(df20)}")
print(len(merged_df))


england_merged = merged_df[merged_df["nationality"] == "England"]
"""
for df in merged_df.columns:
    print(df)
"""
"""
df15 = merged_df.loc[
    :,
    [
        "short_name",
        "long_name",
        "nationality",
        "club_15",
        "age_15",
        "attacking_crossing_15",
        "attacking_finishing_15",
        "attacking_heading_accuracy_15",
        "attacking_short_passing_15",
        "attacking_volleys_15",
        "defending_15",
        "defending_marking_15",
        "defending_sliding_tackle_15",
        "defending_standing_tackle_15",
        "dribbling_15",
        "mentality_aggression_15",
        "mentality_interceptions_15",
        "mentality_penalties_15",
        "mentality_positioning_15",
        "mentality_vision_15",
        "movement_acceleration_15",
        "movement_agility_15",
        "movement_balance_15",
        "movement_reactions_15",
        "movement_sprint_speed_15",
        "pace_15",
        "passing_15",
        "physic_15",
        "power_jumping_15",
        "power_long_shots_15",
        "power_shot_power_15",
        "power_stamina_15",
        "power_strength_15",
        "shooting_15",
        "skill_ball_control_15",
        "skill_curve_15",
        "skill_dribbling_15",
        "skill_fk_accuracy_15",
        "skill_long_passing_15",
        "team_position_15",
        "overall_15",
        "value_eur_15",
    ],
]
print(df15.head())
for col in df15.columns:
    if col.endswith("_15"):
        df15.rename(columns={col: f"{col[:-3]}"}, inplace=True)
print(df15.head())
for df in df15.columns:
    print(df)
"""
