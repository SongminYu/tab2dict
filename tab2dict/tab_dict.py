import math
import os
from typing import List
from typing import Union
from typing import Optional
import pandas as pd


TabDictType = Union["ID", "Relation", "Data"]


class TabDict:
    def __init__(
        self,
        tdict_type: TabDictType,
        key_cols: List[str],
        tdict_data: dict,
    ):
        self.tdict_type = tdict_type
        self.key_cols = key_cols
        self._data = tdict_data

    def __len__(self):
        return len(self._data.items())

    @classmethod
    def from_file(cls, file_path: os.path, value_column_name: str = "value", time_column_name: Optional[str] = None):
        return cls.from_dataframe(
            df=cls._load_file(file_path),
            tdict_type=cls._detect_type(file_path),
            value_column_name=value_column_name,
            time_column_name=time_column_name
        )

    @classmethod
    def from_dataframe(
            cls, df: pd.DataFrame,
            tdict_type: TabDictType,
            value_column_name: str = "value",
            time_column_name: Optional[str] = None
    ):
        assert tdict_type in [
            "ID",
            "Relation",
            "Data",
        ], f"tdict_type must be in [ID, Relation, Data]."
        key_cols = cls._detect_key_cols(df)
        if time_column_name is not None:
            key_cols.append(time_column_name)
            l = []
            index_cols = [col for col in df.columns if col.startswith(("id_", "unit"))]
            time_cols = [col for col in df.columns if not col.startswith(("id_", "unit"))]
            for index, row in df.iterrows():
                for time_col in time_cols:
                    d = {}
                    for index_col in index_cols:
                        d[index_col] = row[index_col]
                    d[time_column_name] = time_col
                    d["value"] = row[time_col]
                    l.append(d)
            df = pd.DataFrame(l)
            df[time_column_name] = df[time_column_name].astype(int)
        tdict_data = cls._generate_tdict_data(
            tdict_type=tdict_type,
            key_cols=key_cols,
            df=df,
            value_column_name=value_column_name,
        )
        return cls._construct_tdict(
            tdict_type=tdict_type,
            key_cols=key_cols,
            tdict_data=tdict_data
        )

    @classmethod
    def _construct_tdict(cls, tdict_type, key_cols, tdict_data):
        if tdict_type == "Relation":
            del key_cols[-1]
        return cls(tdict_type=tdict_type, key_cols=key_cols, tdict_data=tdict_data)

    @classmethod
    def create_empty_data_tdict(cls, key_cols: List[str]):
        return cls(tdict_type="Data", key_cols=key_cols, tdict_data={})

    @staticmethod
    def _detect_type(file_path: str):
        file_name = os.path.basename(file_path)
        assert file_name.startswith(
            ("ID_", "Relation_", "Data_")
        ), "FileName Error: file name must start with 'ID_', 'Relation_', or 'Data_'."
        tdict_type = file_name.split("_")[0]
        return tdict_type

    @staticmethod
    def _detect_key_cols(df: pd.DataFrame):
        return [col for col in list(df.columns) if col.startswith(("id_", "time_"))]

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
    def _generate_tdict_data(
        tdict_type: TabDictType,
        key_cols: List[str],
        df: pd.DataFrame,
        value_column_name,
    ) -> dict:
        d = {}
        if tdict_type == "ID":
            assert (
                "name" in df.columns
            ), "ColumnName Error: column must be called 'name' in 'ID' tables."
            for _, row in df.iterrows():
                d[tuple([row[key_cols[0]]])] = row["name"]
        elif tdict_type == "Relation":
            keys = df[key_cols[0]].unique()
            for key in keys:
                d[tuple([key])] = df.loc[df[key_cols[0]] == key][key_cols[1]].to_list()
        else:
            for _, row in df.iterrows():
                key = []
                for key_col in key_cols:
                    key.append(row[key_col])
                d[tuple(key)] = row[value_column_name]
        return d

    def _tkey2tuple(self, tkey: "TabKey") -> tuple:
        return tuple([int(tkey.__dict__[col]) for col in self.key_cols])

    def get_item(self, tkey: "TabKey", not_found_default=None):
        key = self._tkey2tuple(tkey)
        if key in self._data.keys():
            value = self._data[key]
        else:
            if not_found_default is not None:
                value = not_found_default
            else:
                raise KeyError
        return value

    def set_item(self, tkey: "TabKey", value):
        key = self._tkey2tuple(tkey)
        self._data[key] = value

    def accumulate_item(self, tkey: "TabKey", value):
        key = self._tkey2tuple(tkey)
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
            if key.startswith(("id_", "time_")) and value is not None:
                d[key] = value
        return d
