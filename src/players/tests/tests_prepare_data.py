from lib2to3.pytree import Base
import pytest
import pandas as pd
from pathlib import Path
import sys
from players.core.management.commands.prepare_data import Command

cwd = Path.cwd()
sys.path.append("./players/management/commands")
#from prepare_data import Command

@pytest.fixture
def command():
    return Command()

def test_data_optimization_with_category_and_int_types(command):
    # test to check optimize_types module from prepare_data menagement command
    filepath = "./players/tests/fixtures/remove_gk.csv"
    df = pd.read_csv(filepath)
    df = command.optimize_types(df)
    assert df["club"].dtypes == "category"
    assert df["nationality"].dtypes == "category"
    assert df["age"].dtypes == int


def test_read_csv_with_proper_amount_of_columns(command):
    # test to check reader module from prepare_data menagement command
    filepath = "./players/tests/fixtures/players_16.csv"
    df = command.read_csv(filepath)
    assert len(df.columns) == 42


def test_read_wrong_file(tmpdir, command):
    # test to check raising ValueError extention
    with pytest.raises(BaseException):
        p = tmpdir.mkdir("test_data").join("wrong_file")
        #p.write("nope")
        #p = f"{cwd}/players/data/wrong.txt"
        df = command.read_csv(p)


def test_remove_goalkeepers_if_all_goalkeepers_removed(command):
    # check removing goalkeepers from dataframe
    filepath = "./players/tests/fixtures/reader.csv"
    df = pd.read_csv(filepath)
    df = command.remove_goalkeepers(df)
    df_gk = df[df["player_positions"] == "GK"]
    df_sub = df[df["team_position"] == "SUB"]
    df_res = df[df["team_position"] == "RES"]
    assert len(df_gk) == 0
    assert len(df_sub) == 0
    assert len(df_res) == 0


def test_save_good_file(tmp_path, command):
    # check to save prepared dataframe to csv file inside temporary dict
    filepath = "./players/tests/fixtures/optimize_types.csv"
    df = pd.read_csv(filepath)
    dir_path = tmp_path / "players_temp"
    file_path = tmp_path / "players_temp/2016.csv"
    dir_path.mkdir()
    command.save_file(df, dir_path, "players_16.csv")
    assert Path.is_file(file_path)


def test_good_list_files(command):
    path = "./players/tests/fixtures/"
    list_files = command.list_files(path)
    assert list_files == sorted(list_items)


def test_wrong_list_files(command):
    # check for raise exception when directiory does not exist
    with pytest.raises(BaseException):
        path = "./players/wrong_tests_inputs/"
        list_files = command.list_files(path)


def test_save_file_wrong_dir(tmp_path, command):
    # check to save prepared dataframe to csv file inside wrong dict
    with pytest.raises(BaseException):
        filepath = "./players/tests/fixtures/optimize_types.csv"
        df = pd.read_csv(filepath)
        dir_path = Path("players_wrong")
        file_path = tmp_path / "players_temp/2016.csv"
        command.save_file(df, dir_path, "players_16.csv")


def test_list_files_wrong_dir(command):
    # check to load csv files from not existing dict
    with pytest.raises(BaseException):
        path = "./players/wrong_tests_inputs/"
        list_files = command.list_files(path)
        assert list_files == sorted(list_files)


def test_list_files_not_csv_file(command):
    # check to load csv files from not existing dict
    with pytest.raises(BaseException):
        path = "./players/wrong_tests_inputs/"
        list_files = command.list_files(path)
        assert list_files == sorted(list_files)


def test_handle_input_right_path(tmp_path, command):
    # check handle module by inputing right path and outputing right path
    input = "players/input_data"
    output = tmp_path / "players_temp"
    filepath = tmp_path / "players_temp/2016.csv"
    output.mkdir()
    handle = command.handle(input, output)
    assert Path.is_file(filepath)


def test_handle_input_wrong_path(tmp_path, command):
    # check handle module by inputing right path and outputing right path
    with pytest.raises(BaseException):
        input = "players/input_data_wrong_path"
        output = tmp_path / "players_temp"
        filepath = tmp_path / "players_temp/2016.csv"
        output.mkdir()
        handle = command.handle(input, output)
        Path.is_file(filepath)
