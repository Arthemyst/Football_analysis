import pytest
import pandas as pd

def test_columns_quantity():

    filepath = "./players/data/2015.csv"
    df = pd.read_csv(filepath)
    assert len(df.columns) == 42

def test_example2():
    assert 1 == 1