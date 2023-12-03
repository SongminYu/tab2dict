from tab2dict import TabDict
from tab2dict import TabKey
import pytest
from typing import Optional


class TestTabKey(TabKey):
    def __init__(
        self,
        id_position: Optional[int] = None,
        id_project_type: Optional[int] = None,
    ):
        self.id_position = id_position
        self.id_project_type = id_project_type


@pytest.fixture
def id_tdict():
    td = TabDict.from_path("tests/data/ID_Position.xlsx")
    return td


@pytest.fixture
def relation_tdict():
    td = TabDict.from_path("tests/data/Relation_Position_ProjectType.xlsx")
    return td


@pytest.fixture
def data_tdict():
    td = TabDict.from_path("tests/data/Data_ProjectSize.xlsx")
    print()
    return td


def test_tab_dict_type(id_tdict, relation_tdict, data_tdict):
    assert id_tdict.tab_dict_type == "ID"
    assert relation_tdict.tab_dict_type == "Relation"
    assert data_tdict.tab_dict_type == "Data"


def test_get_item(id_tdict, relation_tdict, data_tdict):
    tkey = TestTabKey(id_position=1, id_project_type=2)
    assert id_tdict.get_item(tkey) == "Full Prof."
    assert relation_tdict.get_item(tkey) == [1, 2, 3]
    assert data_tdict.get_item(tkey) == 200


def test_set_item():
    tkey = TestTabKey(id_position=1, id_project_type=2)
    tdict = TabDict.empty(key_cols=["id_position", "id_project_type"])
    tdict.set_item(tkey, 500)
    assert tdict.get_item(tkey) == 500


def test_accumulate_item():
    tkey = TestTabKey(id_position=1, id_project_type=2)
    tdict = TabDict.empty(key_cols=["id_position", "id_project_type"])
    tdict.accumulate_item(tkey, 500)
    tdict.accumulate_item(tkey, 300)
    assert tdict.get_item(tkey) == 800
