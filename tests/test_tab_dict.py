import os

import pandas as pd

from tab2dict import TabDict
from tab2dict import TabKey
import pytest
from typing import Optional


class BuildingTabKey(TabKey):
    def __init__(
        self,
        id_sector: Optional[int] = None,
        id_building_type: Optional[int] = None,
        time_year: Optional[int] = None,
    ):
        self.id_sector = id_sector
        self.id_building_type = id_building_type
        self.time_year = time_year


DATA_FOLDER = "tests/data"


@pytest.fixture
def id_tdict():
    td = TabDict.from_file(os.path.join(DATA_FOLDER, "ID_Sector.xlsx"))
    return td


@pytest.fixture
def relation_tdict():
    td = TabDict.from_file(
        os.path.join(DATA_FOLDER, "Relation_Sector_BuildingType.xlsx")
    )
    return td


@pytest.fixture
def data_tdict():
    td = TabDict.from_file(os.path.join(DATA_FOLDER, "Data_BuildingStock.xlsx"))
    return td


@pytest.fixture
def time_data_tdict():
    td = TabDict.from_file(os.path.join(DATA_FOLDER, "Data_EnergyIntensityIndex.xlsx"))
    return td


@pytest.fixture
def time_data_wide_tdict():
    td = TabDict.from_file(
        os.path.join(DATA_FOLDER, "Data_EnergyIntensityIndex_Wide.xlsx"),
        time_column_name="time_year"
    )
    return td


@pytest.fixture
def multi_col_data_tdict_a():
    td = TabDict.from_file(
        os.path.join(DATA_FOLDER, "Data_BuildingParameter.xlsx"), value_column_name="a"
    )
    return td


@pytest.fixture
def multi_col_data_tdict_b():
    td = TabDict.from_file(
        os.path.join(DATA_FOLDER, "Data_BuildingParameter.xlsx"), value_column_name="b"
    )
    return td


@pytest.fixture
def multi_col_data_tdict_c():
    td = TabDict.from_file(
        os.path.join(DATA_FOLDER, "Data_BuildingParameter.xlsx"), value_column_name="c"
    )
    return td


@pytest.fixture
def df_data_tdict():
    df = pd.DataFrame(
        {
            "id_sector": [1, 1, 2, 3, 4],
            "id_building_type": [1, 2, 6, 4, 5],
            "unit": "count",
            "value": [10, 20, 30, 40, 50],
        }
    )
    td = TabDict.from_dataframe(df=df, tdict_type="Data")
    return td


def test_tab_dict_type(id_tdict, relation_tdict, data_tdict, time_data_tdict):
    assert id_tdict.tdict_type == "ID"
    assert relation_tdict.tdict_type == "Relation"
    assert data_tdict.tdict_type == "Data"
    assert time_data_tdict.tdict_type == "Data"


def test_get_item(id_tdict, relation_tdict, data_tdict, time_data_tdict, time_data_wide_tdict):
    tkey = BuildingTabKey(id_sector=1, id_building_type=2, time_year=2030)
    assert id_tdict.get_item(tkey) == "residential"
    assert relation_tdict.get_item(tkey) == [1, 2]
    assert data_tdict.get_item(tkey) == 12000
    assert time_data_tdict.get_item(tkey) == 0.98
    assert time_data_wide_tdict.get_item(tkey) == 0.98


def test_multi_col_data(
    multi_col_data_tdict_a, multi_col_data_tdict_b, multi_col_data_tdict_c
):
    tkey = BuildingTabKey(id_sector=3, id_building_type=4)
    assert multi_col_data_tdict_a.get_item(tkey) == 7
    assert multi_col_data_tdict_b.get_item(tkey) == 70
    assert multi_col_data_tdict_c.get_item(tkey) == 700


def test_tdict_from_dataframe(df_data_tdict):
    tkey = BuildingTabKey(id_sector=3, id_building_type=4)
    assert df_data_tdict.get_item(tkey) == 40


def test_create_empty_data_tdict():
    tdict = TabDict.create_empty_data_tdict(key_cols=["id_sector", "id_building_type"])
    assert type(tdict) is TabDict


def test_set_item_and_to_dataframe():
    tkey = BuildingTabKey(id_sector=1, id_building_type=2, time_year=2030)
    tdict = TabDict.create_empty_data_tdict(key_cols=["id_sector", "id_building_type"])
    tdict.set_item(tkey, 500)
    assert tdict.get_item(tkey) == 500
    assert type(tdict.to_dataframe()) is pd.DataFrame


def test_accumulate_item():
    tkey = BuildingTabKey(id_sector=1, id_building_type=2, time_year=2030)
    tdict = TabDict.create_empty_data_tdict(
        key_cols=["id_sector", "id_building_type", "time_year"]
    )
    tdict.accumulate_item(tkey, 500)
    tdict.accumulate_item(tkey, 300)
    assert tdict.get_item(tkey) == 800
