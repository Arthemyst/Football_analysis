from pathlib import Path

import pandas as pd
import pytest
from players.constants import DEFAULT_COLUMNS, UNOPTIMIZABLE_COLUMNS
from players.exceptions import NoFilesException

from players.management.commands.add_data import Command


@pytest.fixture
def command():
    return Command()

def test_read_csv_with_proper_amount_of_columns(command):
    # test to check reader module from prepare_data management command
    filepath = Path("players/tests/fixtures/players_16.csv")
    df = command.read_csv(filepath)

    assert len(df.columns) == 42

