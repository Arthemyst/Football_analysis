from pathlib import Path

import pandas as pd
import pytest
from players.constants import DEFAULT_COLUMNS, UNOPTIMIZABLE_COLUMNS
from players.exceptions import (NoFilesException,
                                NotExistingDirectoryException)
from players.management.commands.prepare_data import Command


@pytest.fixture
def command():
    return Command()


def test_data_optimization_with_category_and_int_types(command):
    # test to check optimize_types module from prepare_data management command
    filepath = Path(
        "players/tests/fixtures/test_csv_file_after_removing_goalkeepers.csv"
    )
    df = command.read_csv(filepath)
    df = command.optimize_types(df, filepath)

    assert df["club"].dtypes == "category"
    assert df["age"].dtypes == int


def test_read_csv_with_proper_amount_of_columns(command):
    # test to check reader module from prepare_data management command
    filepath = Path("players/tests/fixtures/players_16.csv")
    df = command.read_csv(filepath)

    assert len(df.columns) == 42


def test_remove_goalkeepers_if_all_goalkeepers_removed(command):
    # check removing goalkeepers from dataframe
    df = command.read_csv(
        Path("players/tests/fixtures/test_csv_file_for_testing_reading_module.csv")
    )
    df = command.remove_goalkeepers(df)

    assert len(df[df["player_positions"] == "GK"]) == 0
    assert len(df[df["team_position"] == "SUB"]) == 0
    assert len(df[df["team_position"] == "RES"]) == 0


def test_save_good_file(tmp_path, command):
    # check to save prepared dataframe to csv file inside temporary dict
    filepath = "players/tests/fixtures/test_csv_file_after_types_optimization.csv"
    df = pd.read_csv(filepath)
    dir_path = tmp_path / "players_temp"
    file_path = tmp_path / "players_temp/players_16.csv"
    dir_path.mkdir()

    command.save_file(df, dir_path, file_path)

    assert Path.is_file(file_path) and Path.exists(Path(file_path))


def test_list_files_returns_csv_files(command, tmp_path):
    path = "players/tests/fixtures"

    list_csv_files = command.list_csv_files(path)

    assert list_csv_files == sorted(list_csv_files)


def test_list_files_raises_on_nonexistent_directory(command):
    # check for raise exception when directiory does not exist
    path = "players/wrong_tests_inputs"

    with pytest.raises(NoFilesException, match="No such file or directory"):
        list_files = command.list_csv_files(path)


def test_save_file_wrong_dir(tmp_path, command):
    # check to save prepared dataframe to csv file inside wrong dir
    dir_path = Path("players_wrong")
    file_path = tmp_path / "players_temp/players_2016.csv"
    filepath = "players/tests/fixtures/test_csv_file_after_types_optimization.csv"
    df = pd.read_csv(filepath)

    with pytest.raises(
        NotExistingDirectoryException,
        match="Cannot save file into a non-existent directory",
    ):
        command.save_file(df, dir_path, file_path)


def test_list_files_not_csv_file(command):
    # check to load csv files from not existing dir
    path = "players/wrong_tests_inputs/"

    with pytest.raises(NoFilesException, match="No such file or directory"):
        list_files = command.list_csv_files(path)


def test_handle_input_right_path(tmp_path, command):
    # check handle module by inputing right path and outputing right path
    input = "players/tests/fixtures/test_handle_input_right_path"
    output = tmp_path / "players_temp"
    output.mkdir()
    filepath = tmp_path / "players_temp/players_16.csv"

    command.handle(input, output)

    assert Path.is_file(filepath)


def test_handle_input_wrong_path(tmp_path, command):
    # check handle module by inputing wrong path and outputing right path
    input = "players/input_data_wrong_path"
    output = tmp_path / "players_temp"
    filepath = tmp_path / "players_temp/players_16.csv"

    with pytest.raises(NoFilesException, match="No such file or directory"):
        handle = command.handle(input, output)
