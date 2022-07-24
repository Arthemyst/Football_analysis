DEFAULT_COLUMNS = [
    "short_name",
    "long_name",
    "nationality",
    "club",
    "team_position",
    "player_positions",
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
    "overall",
    "value_eur",
]

UNOPTIMIZABLE_COLUMNS = [
    "player_positions",
    "team_position",
    "short_name",
    "club",
    "nationality",
    "long_name",
]

VALUES_COLUMNS = [
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
    "overall",
    "value_eur",
]

MIDFIELD_POSITION_COLUMNS = [
    "CAM",
    "RM",
    "RDM",
    "LDM",
    "LCM",
    "CDM",
    "LAM",
    "RAM",
    "CM",
    "RCM",
]
ATTACK_POSITION_COLUMNS = ["RW", "LM", "ST", "LW", "LF", "RF", "LS", "RS", "CF"]
DEFEND_POSITION_COLUMNS = ["RCB", "CB", "LCB", "LWB", "RWB", "RB", "LB"]

DEFEND_COLUMNS_FOR_ESTIMATION =                    [
                        "defending",
                        "defending_marking",
                        "defending_sliding_tackle",
                        "defending_standing_tackle",
                        "mentality_interceptions",
                        "movement_reactions",
                        "value_eur",
                    ]

ATTACK_COLUMNS_FOR_ESTIMATION =                     [
                        "attacking_finishing",
                        "attacking_short_passing",
                        "dribbling",
                        "mentality_positioning",
                        "movement_reactions",
                        "passing",
                        "shooting",
                        "skill_ball_control",
                        "skill_dribbling",
                        "value_eur",
                    ]

MIDFIELD_COLUMNS_FOR_ESTIMATION =                     [
                        "attacking_short_passing",
                        "dribbling",
                        "mentality_positioning",
                        "mentality_vision",
                        "movement_reactions",
                        "passing",
                        "shooting",
                        "skill_ball_control",
                        "skill_dribbling",
                        "skill_long_passing",
                        "value_eur",
                    ]

random_grid = {'bootstrap': [True, False],
               'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, None],
               'max_features': ['auto', 'sqrt'],
               'min_samples_leaf': [1, 2, 4],
               'min_samples_split': [2, 5, 10],
               'n_estimators': [130, 180, 230]}
               