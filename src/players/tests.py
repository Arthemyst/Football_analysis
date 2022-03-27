import pytest
import pandas as pd
from pathlib import Path
import sys
import os
from io import StringIO

cwd = Path.cwd()
# importing sys


sys.path.append("./players/management/commands")
# from prepare_data import Command
from prepare_data import Command


def test_data_optimization():
    # test to check optimize_types module from prepare_data menagement command
    filepath = "./players/tests_inputs/remove_gk.csv"
    df = pd.read_csv(filepath)
    df = Command().optimize_types(df)
    assert df["club"].dtypes == "category"
    assert df["nationality"].dtypes == "category"
    assert df["age"].dtypes == int


def test_read_csv():
    # test to check reader module from prepare_data menagement command
    filepath = "./players/tests_inputs/players_16.csv"
    df = Command().read_csv(filepath)
    assert len(df.columns) == 42


def test_read_wrong_file(tmpdir):
    # test to check raising ValueError extention
    with pytest.raises(ValueError):
        p = tmpdir.mkdir("test_data").join("wrong_file")
        # p.write("nope")
        # p = f"{cwd}/players/data/wrong.txt"
        df = Command().read_csv(p)


def test_remove_goalkeepers():
    # check removing goalkeepers from dataframe
    filepath = "./players/tests_inputs/reader.csv"
    df = pd.read_csv(filepath)
    df = Command().remove_goalkeepers(df)
    df_gk = df[df["player_positions"] == "GK"]
    df_sub = df[df["team_position"] == "SUB"]
    df_res = df[df["team_position"] == "RES"]
    assert len(df_gk) == 0
    assert len(df_sub) == 0
    assert len(df_res) == 0


def test_save_good_file(tmp_path):
    # check to save prepared dataframe to csv file inside temporary dict
    filepath = "./players/tests_inputs/optimize_types.csv"
    df = pd.read_csv(filepath)
    dir_path = tmp_path / "players_temp"
    file_path = tmp_path / "players_temp/2016.csv"
    dir_path.mkdir()
    Command().save_file(df, dir_path, "players_16.csv")
    assert Path.is_file(file_path)


def test_list_items():
    path = "./players/tests_inputs/"
    list_items = Command().list_items(path)
    assert list_items == sorted(list_items)


def test_wrong_list_items():
    # check for raise exception when directiory does not exist
    with pytest.raises(FileNotFoundError):
        path = "./players/wrong_tests_inputs/"
        list_items = Command().list_items(path)


def test_save_file_wrong_dir(tmp_path):
    # check to save prepared dataframe to csv file inside wrong dict
    with pytest.raises(OSError):
        filepath = "./players/tests_inputs/optimize_types.csv"
        df = pd.read_csv(filepath)
        dir_path = Path("players_wrong")
        file_path = tmp_path / "players_temp/2016.csv"
        Command().save_file(df, dir_path, "players_16.csv")


def test_list_items_wrong_dir():
    # check to load csv files from not existing dict
    with pytest.raises(FileNotFoundError):
        path = "./players/wrong_tests_inputs/"
        list_items = Command().list_items(path)
        assert list_items == sorted(list_items)


def test_list_items_not_csv_file():
    # check to load csv files from not existing dict
    with pytest.raises(FileNotFoundError):
        path = "./players/wrong_tests_inputs/"
        list_items = Command().list_items(path)
        assert list_items == sorted(list_items)


def test_handle_input_right_path(tmp_path):
    # check handle module by inputing right path and outputing right path
    input = "players/input_data"
    output = tmp_path / "players_temp"
    filepath = tmp_path / "players_temp/2016.csv"
    output.mkdir()
    handle = Command().handle(input, output)
    assert Path.is_file(filepath)


def test_handle_input_wrong_path(tmp_path):
    # check handle module by inputing right path and outputing right path
    with pytest.raises(FileNotFoundError):
        input = "players/input_data_wrong_path"
        output = tmp_path / "players_temp"
        filepath = tmp_path / "players_temp/2016.csv"
        output.mkdir()
        handle = Command().handle(input, output)
        Path.is_file(filepath)


"""
def test_add_arguments():
    command = Command()
    input_path = "players/input_data"
    output_path = "players/data"
    parser = command.add_arguments(input_path)

    assert parser[0] == "players/input_data"
    #assert parser[1] == "players/data"

    out = StringIO()
    call_command(
        "normalize_book_titles",
        *args,
        stdout=out,
        stderr=StringIO(),
        **kwargs,
    )
    return out.getvalue()
"""
