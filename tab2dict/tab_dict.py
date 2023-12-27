import math
import os
from typing import List
from typing import Union

import pandas as pd


TabDictType = Union["ID", "Relation", "Data"]


# TODO: add cache to improve the speed (like RENDER)

class TabDict:
    def __init__(
        self,
        tab_dict_type: TabDictType,
        key_cols: List[str],
        tab_dict_data: dict,
    ):
        super().__init__()
        self.tab_dict_type = tab_dict_type
        self.key_cols = key_cols
        self._data = tab_dict_data

    def __len__(self):
        return len(self._data.items())

    @classmethod
    def from_path(cls, file_path: os.path):
        file_name = file_path.split("/")[-1]
        assert file_name.startswith(
            ("ID_", "Relation_", "Data_")
        ), "FileName Invalid: must start with 'ID_', 'Relation_', or 'Data_'."
        tab_dict_type = file_name.split("_")[0]
        df = cls._load_file(file_path)
        key_cols = [
            col
            for col in list(df.columns)
            if col.startswith("id_") or col.startswith("period")
        ]
        tab_dict_data = cls._generate_tab_dict_data(
            tab_dict_type=tab_dict_type, key_cols=key_cols, df=df
        )
        if tab_dict_type == "Relation":
            del key_cols[-1]
        return cls(
            tab_dict_type=tab_dict_type, key_cols=key_cols, tab_dict_data=tab_dict_data
        )

    @classmethod
    def from_dataframe(
        cls, tab_dict_type: TabDictType, key_cols: List[str], df: pd.DataFrame
    ):
        assert tab_dict_type in [
            "ID",
            "Relation",
            "Data",
        ], f"TabDictType Invalid: {tab_dict_type} not supported."
        tab_dict_data = cls._generate_tab_dict_data(
            tab_dict_type=tab_dict_type, key_cols=key_cols, df=df
        )
        return cls(
            tab_dict_type=tab_dict_type, key_cols=key_cols, tab_dict_data=tab_dict_data
        )

    @classmethod
    def empty(cls, key_cols: List[str], tab_dict_type: TabDictType = "Data"):
        return cls(tab_dict_type=tab_dict_type, key_cols=key_cols, tab_dict_data={})

    @staticmethod
    def _load_file(file_path: os.path) -> pd.DataFrame:
        ext = file_path.split(".")[-1]
        assert ext in [
            "xls",
            "xlsx",
            "csv",
        ], f"FileType Error: .{ext} input not supported."
        if ext in {"xls", "xlsx"}:
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
        return df

    @staticmethod
    def _generate_tab_dict_data(
        tab_dict_type: TabDictType, key_cols: List[str], df: pd.DataFrame
    ) -> dict:
        assert tab_dict_type in [
            "ID",
            "Relation",
            "Data",
        ], f"TabDictType Invalid: {tab_dict_type} not supported."
        d = {}
        if tab_dict_type == "ID":
            assert (
                "name" in df.columns
            ), "ColumnName Error: column must be called 'name' in 'ID' tables."
            for _, row in df.iterrows():
                d[tuple([row[key_cols[0]]])] = row["name"]
        elif tab_dict_type == "Relation":
            keys = df[key_cols[0]].unique()
            for key in keys:
                d[tuple([key])] = df.loc[df[key_cols[0]] == key][key_cols[1]].to_list()
        else:
            assert (
                "value" in df.columns
            ), "ColumnName Error: column must be called 'value' in 'Data' tables."
            for _, row in df.iterrows():
                key = []
                for key_col in key_cols:
                    key.append(row[key_col])
                    d[tuple(key)] = row["value"]
        return d

    def tkey2tuple(self, tkey: "TabKey") -> tuple:
        return tuple([int(tkey.__dict__[col]) for col in self.key_cols])

    def get_item(self, tkey: "TabKey", not_found_default=None):
        key = self.tkey2tuple(tkey)
        if key in self._data.keys():
            value = self._data[key]
        else:
            if not_found_default is not None:
                value = not_found_default
            else:
                raise KeyError
        return value

    def set_item(self, tkey: "TabKey", value):
        key = self.tkey2tuple(tkey)
        self._data[key] = value

    def accumulate_item(self, tkey: "TabKey", value):
        key = self.tkey2tuple(tkey)
        if key in self._data.keys():
            self._data[key] = self._data[key] + value
        else:
            self._data[key] = value

    def to_dataframe(self):
        l = []
        for key_ids, value in self._data.items():
            d = dict(zip(self.key_cols, key_ids))
            d["value"] = value
            l.append(d)
        return pd.DataFrame(l)


class TabKey:
    def from_dict(self, d: dict):
        for key, value in d.items():
            if key in self.__dict__.keys():
                self.__setattr__(key, value)
        return self

    @property
    def key_cols(self):
        key_cols = []
        for key, value in self.__dict__.items():
            if value is not None:
                key_cols.append(key)
        return key_cols

    def make_copy(self):
        rk = self.__class__()
        for k, v in self.__dict__.items():
            rk.__dict__[k] = v
        return rk

    def filter_dataframe(self, df: pd.DataFrame):
        query = ""
        for key, value in self.__dict__.items():
            if (
                key.startswith("id")
                and value is not None
                and not math.isnan(value)
                and key in list(df.columns)
            ):
                query += f"`{key}` == {value} and "
        return df.query(query[:-5])

    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if value is not None:
                d[key] = value
        return d
