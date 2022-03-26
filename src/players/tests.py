import pytest
import pandas as pd
from pathlib import Path
import sys
import os

cwd = Path.cwd()
# importing sys


sys.path.append("./players/management/commands")
# from prepare_data import Command
from prepare_data import Command


def test_data_optimization():
    # test to check optimize_types module from prepare_data menagement command
    command = Command()
    filepath = "./players/tests_inputs/remove_gk.csv"
    df = pd.read_csv(filepath)
    df = command.optimize_types(df)
    assert df["club"].dtypes == "category"
    assert df["nationality"].dtypes == "category"
    assert df["age"].dtypes == int


def test_read_csv():
    # test to check reader module from prepare_data menagement command

    command = Command()
    filepath = "./players/tests_inputs/players_16.csv"
    df = command.read_csv(filepath)
    assert len(df.columns) == 42


def test_remove_goalkeepers():
    # check removing goalkeepers from dataframe
    command = Command()
    filepath = "./players/tests_inputs/reader.csv"
    df = pd.read_csv(filepath)
    df = command.remove_goalkeepers(df)
    df_gk = df[df["player_positions"] == "GK"]
    df_sub = df[df["team_position"] == "SUB"]
    df_res = df[df["team_position"] == "RES"]
    assert len(df_gk) == 0
    assert len(df_sub) == 0
    assert len(df_res) == 0


def test_save_good_file(tmp_path):
    # check to save prepared dataframe to csv file inside temporary dict
    command = Command()
    filepath = "./players/tests_inputs/optimize_types.csv"
    df = pd.read_csv(filepath)
    dir_path = tmp_path / "players_temp"
    file_path = tmp_path / "players_temp/2016.csv"
    dir_path.mkdir()
    command.save_file(df, dir_path, "players_16.csv")
    assert Path.is_file(file_path) == True


def test_list_items():
    command = Command()
    path = "./players/tests_inputs/"
    list_items = command.list_items(path)
    assert list_items == sorted(list_items)


def test_input_path(tmpdir_factory):

    pass


def test_save_file_wrong_dir(tmp_path):
    # check to save prepared dataframe to csv file inside temporary dict
    with pytest.raises(OSError):
        command = Command()
        filepath = "./players/tests_inputs/optimize_types.csv"
        df = pd.read_csv(filepath)
        dir_path = Path("players_wrong")
        file_path = tmp_path / "players_temp/2016.csv"
        command.save_file(df, dir_path, "players_16.csv")


def test_list_items_wrong_dir():
    with pytest.raises(FileNotFoundError):
        command = Command()
        path = "./players/wrong_tests_inputs/"
        list_items = command.list_items(path)
        assert list_items == sorted(list_items)
