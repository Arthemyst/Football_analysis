from pathlib import Path

import numpy
import pandas as pd
import pytest

import sklearn
from players.constants import ATTACK_COLUMNS_FOR_ESTIMATION
from players.exceptions import NoFilesException, NotExistingDirectoryException
from players.management.commands.prepare_estimation_models import Command


@pytest.fixture
def command():
    return Command()


def test_list_csv_files_succeed(command):
    path = "players/tests/fixtures/list_csv_files"
    list_csv_files = command.list_csv_files(path)

    assert list_csv_files == sorted(list_csv_files)


def test_list_files_not_csv_file(command):
    # check to load csv files from not existing dir
    path = "players/wrong_tests_inputs/"

    with pytest.raises(NoFilesException, match="No such file or directory"):
        list_files = command.list_csv_files(path)


def test_read_csv_with_proper_amount_of_columns(command):
    # test to check reader module from add_data management command
    filepath = Path("players/tests/fixtures/players_file_to_model_estimation.csv")
    df = command.read_csv(filepath)

    assert len(df.columns) == 44


def test_list_files_raises_on_nonexistent_directory(command):
    # check for raise exception when directiory does not exist
    path = "players/wrong_tests_inputs"

    with pytest.raises(NoFilesException, match="No such file or directory"):
        list_files = command.list_csv_files(path)


def test_model_to_estimate_player_value_with_succeed(command):
    filepath = Path("players/tests/fixtures/players_file_to_model_estimation.csv")
    dataframe = command.read_csv(filepath)
    model = command.model_to_estimate_player_value(
        dataframe, ATTACK_COLUMNS_FOR_ESTIMATION
    )
    assert type(model[1]) == numpy.float64
    assert type(model[0]) == sklearn.ensemble._forest.RandomForestRegressor


def test_position_filter_succeed_remove_rows_with_value_eur_equal_zero(command):
    filepath = Path(
        "players/tests/fixtures/players_file_to_model_estimation_with_value_eur_equal_zero.csv"
    )
    dataframe = command.read_csv(filepath)
    dataframe_after_position_filter = command.position_filter("attackers", dataframe)
    assert len(dataframe_after_position_filter) == 3


def test_model_creation_succeed(command):
    filepath = Path("players/tests/fixtures/players_file_to_model_estimation.csv")

    dataframe = command.read_csv(filepath)

    dataframe_after_position_filter = command.position_filter("attackers", dataframe)
    attack_models_list = []
    command.model_creation(
        dataframe_after_position_filter,
        "attackers",
        ATTACK_COLUMNS_FOR_ESTIMATION,
        attack_models_list,
    )
    assert len(attack_models_list) == 1
    assert (
        type(attack_models_list[0][0]) == sklearn.ensemble._forest.RandomForestRegressor
    )
    assert type(attack_models_list[0][1]) == float


def test_handle_input_wrong_path(tmp_path, command):
    # check handle module by inputing wrong path and outputing right path
    input = "players/input_data_wrong_path"
    output = tmp_path / "players_temp"
    filepath = tmp_path / "players_temp/players_16.csv"

    with pytest.raises(NoFilesException, match="No such file or directory"):
        handle = command.handle(input, output)


def test_handle_input_right_path(tmp_path, command):
    # check handle module by inputing right path and outputing right path
    input = "players/tests/fixtures/test_handle_input_right_path_for_prepare_estimation_models"
    output = tmp_path / "models_temp"
    output.mkdir()
    command.handle(input, output)
    list_of_files = [
        item
        for item in Path(output).iterdir()
        if item.is_file() and item.name.endswith(".pkl")
    ]
    assert len(list_of_files) == 3
