from pathlib import Path
import pytest
from players.management.commands.add_data import Command
from players.models import Player
from players.exceptions import NoFilesException

@pytest.fixture
def command():
    return Command()

def test_list_csv_files_succeed(command):
    path = "players/tests/fixtures/list_csv_files"
    list_csv_files = command.list_csv_files(path)

    assert list_csv_files == sorted(list_csv_files)

def test_read_csv_with_proper_amount_of_columns(command):
    # test to check reader module from add_data management command
    filepath = Path("players/tests/fixtures/players_ready_to_load_to_database.csv")
    df = command.read_csv(filepath)

    assert len(df.columns) == 44

@pytest.mark.django_db
def test_load_players_to_db_with_succeed(command):
    
    filepath = Path("players/tests/fixtures/players_ready_to_load_to_database.csv")
    df = command.read_csv(filepath)
    players = command.load_to_db(df)
    player_1 = Player.objects.get(short_name="L. Messi")
    player_2 = Player.objects.get(short_name="Cristiano Ronaldo")
    player_3 = Player.objects.get(short_name="L. Suárez")
    assert player_1.long_name == "Lionel Andrés Messi Cuccittini"
    assert player_2.long_name == "Cristiano Ronaldo dos Santos Aveiro"
    assert player_3.long_name == "Luis Alberto Suárez Díaz"

    player_1.delete()
    player_2.delete()
    player_3.delete()
    

def test_list_files_raises_on_nonexistent_directory(command):
    # check for raise exception when directiory does not exist
    path = "players/wrong_tests_inputs"

    with pytest.raises(NoFilesException, match="No such file or directory"):
        list_files = command.list_csv_files(path)
        