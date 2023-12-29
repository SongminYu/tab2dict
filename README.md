# Readme

`tab2dict` is a tool supporting data handling in developing scientific software (i.e., models). 
The tool can convert predefined input tables (`.xlsx` or `.csv`) into `TabDict` instances.
Then, the items therein can be fetched by `TabKey` instances.

There are two main advantages of using `tab2dict`:
* It allows the users to adapt the input tables relatively freely (e.g., adding or removing index columns) with limited changes in the code.
* As the tables are converted to dictionaries, the fetching speed is faster. With `TabKey`, the readability is also better.

## Getting started

Most functions of `tab2dict` are clearly shown in the test files. 
Below is a quick introduction of the main points.

### TabDict

There are three types of predefined input tables that can be loaded and converted to `TabDict` instances:

* "ID" tables named as "ID_XXX"
* "Relation" tables named as "Relation_XXX"
* "Data" tables named as "Data_XXX"

In each type of tables, the column names must follow the convention shown in the examples below:

**First, in the "ID" tables:**

* The name of the first column must start with `id_`, e.g., `id_sector` or `id_building_type`.
* The name of the second column must be `name`.

Example: `ID_Sector.xlsx`

| id_sector | name                  |
|-----------|-----------------------|
| 1         | residential           |
| 2         | manufacturing         |
| 3         | retail                |
| 4         | hotel and restaurant  |
| 5         | public administration |

Example: `ID_BuildingType.xlsx`

| id_building_type | name                                   |
|------------------|----------------------------------------|
| 1                | single family house                    |
| 2                | multiple family house                  |
| 3                | office                                 |
| 4                | Shopping mall                          |
| 5                | accommodation and restaurant buildings |
| 6                | production buildings                   |
| 7                | other buildings                        |

**Second, in the "Relation" tables:**

* There can only be two columns, showing the relation between the two indexes.

Example: `Relation_Sector_BuildingType.xlsx`

| id_sector | id_building_type |
|-----------|------------------|
| 1         | 1                |
| 1         | 2                |
| 2         | 3                |
| 2         | 6                |
| 2         | 7                |
| 3         | 3                |
| 3         | 4                |
| 4         | 5                |
| 5         | 3                |
| 5         | 5                |
| 5         | 7                |

**Third, in the "Data" tables:**

* `tab2dict` supports multiple index columns in a "Data" table. And, apart from `id_`, `tab2dict` also has `time_` as a known prefix for index column names, designed for timeseries data. But, there is no third known prefix. So, all index columns must have names starting with either `id_` or `time_`. Or, they will not be identified as index columns.
* The `unit` column is optional but suggested to be included.
* By default, the name of the last "value column" is `value`. `tab2dict` also allows users to define other names for the "value column". Besides, the users can have multiple value columns in one "Data" table. For such tables, users should specify the `value_column_name` when loading the table and converting it to an instance of `TabDict` (example below).

Example: `Data_BuildingStock.xlsx`

| id_sector | id_building_type | unit  | value |
|-----------|------------------|-------|-------|
| 1         | 1                | count | 10000 |
| 1         | 2                | count | 12000 |
| 2         | 3                | count | 500   |
| 2         | 6                | count | 3000  |
| 2         | 7                | count | 200   |
| 3         | 3                | count | 300   |
| 3         | 4                | count | 2000  |
| 4         | 5                | count | 2500  |
| 5         | 3                | count | 800   |
| 5         | 5                | count | 100   |
| 5         | 7                | count | 400   |

Example: `Data_EnergyIntensityIndex.xlsx`

| id_building_type | time_year | unit  | value | 
|------------------|-----------|-------|-------|
| 1                | 2020      | Euros | 1     |
| 1                | 2030      | Euros | 0.99  |
| 1                | 2040      | Euros | 0.98  |
| 1                | 2050      | Euros | 0.97  |
| 2                | 2020      | Euros | 1     |
| 2                | 2030      | Euros | 0.98  |
| 2                | 2040      | Euros | 0.96  |
| 2                | 2050      | Euros | 0.94  |
| 3                | 2020      | Euros | 1     |
| 3                | 2030      | Euros | 0.97  |
| 3                | 2040      | Euros | 0.94  |
| 3                | 2050      | Euros | 0.91  |
| 4                | 2020      | Euros | 1     |
| 4                | 2030      | Euros | 0.96  |
| 4                | 2040      | Euros | 0.92  |
| 4                | 2050      | Euros | 0.88  |
| 5                | 2020      | Euros | 1     |
| 5                | 2030      | Euros | 0.95  |
| 5                | 2040      | Euros | 0.9   |
| 5                | 2050      | Euros | 0.85  |
| 6                | 2020      | Euros | 1     |
| 6                | 2030      | Euros | 0.94  |
| 6                | 2040      | Euros | 0.88  |
| 6                | 2050      | Euros | 0.82  |
| 7                | 2020      | Euros | 1     |
| 7                | 2030      | Euros | 0.93  |
| 7                | 2040      | Euros | 0.86  |
| 7                | 2050      | Euros | 0.79  |

Example: `Data_BuildingParameter.xlsx`

| id_sector | id_building_type | unit  | a  | b   | c    |
|-----------|------------------|-------|----|-----|------|
| 1         | 1                | count | 1  | 10  | 100  |
| 1         | 2                | count | 2  | 20  | 200  |
| 2         | 3                | count | 3  | 30  | 300  |
| 2         | 6                | count | 4  | 40  | 400  |
| 2         | 7                | count | 5  | 50  | 500  |
| 3         | 3                | count | 6  | 60  | 600  |
| 3         | 4                | count | 7  | 70  | 700  |
| 4         | 5                | count | 8  | 80  | 800  |
| 5         | 3                | count | 9  | 90  | 900  |
| 5         | 5                | count | 10 | 100 | 1000 |
| 5         | 7                | count | 11 | 110 | 1100 |

### TabKey

`tab2dict` provides the base class `TabKey` that has to be inherited and extended according to the input table columns. 

```python
from tab2dict import TabKey

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
```

As shown, the attributes of the `BuildingTabKey` class are the index column names in the input tables. 
As mentioned, they must always start with `id_` or `time_`.

### Examples

#### Loading data

Users can load and convert a data file to a `TabDict` instance (`tdict`) by calling the `from_file` function.
The index columns will be automatically identified and recorded as its `key_cols`.

```python
from tab2dict import TabDict

sectors = TabDict.from_file("ID_Sector.xlsx")
building_types = TabDict.from_file("ID_BuildingType.xlsx")
relation_sector_building_type = TabDict.from_file("Relation_Sector_BuildingType.xlsx")
building_stock = TabDict.from_file("Data_BuildingStock.xlsx")
energy_intensity_index = TabDict.from_file("Data_EnergyIntensityIndex.xlsx")
building_parameter_a = TabDict.from_file("Data_BuildingParameter.xlsx", value_column_name="a")
building_parameter_b = TabDict.from_file("Data_BuildingParameter.xlsx", value_column_name="b")
building_parameter_c = TabDict.from_file("Data_BuildingParameter.xlsx", value_column_name="c")
```

Besides, users can also use the `from_dataframe` function to create a `tdict`, 
but the `tdict_type` must be specified as `ID`, `Relation`, or `Data`.

```python
from tab2dict import TabDict
import pandas as pd

df = pd.DataFrame({
    "id_sector": [1, 1, 2, 3, 4],
    "id_building_type": [1, 2, 6, 4, 5],
    "unit": "count",
    "value": [10, 20, 30, 40, 50]
})
building_number = TabDict.from_dataframe(df=df, tdict_type="Data")
```

#### Get data

With a `TabKey` instance (`tkey`), users can fetch data from a `tdict`, as long as the `tkey` has values for the `tdict`'s `key_cols`. 
The `tkey` can know more than necessary, which supports the following flexibilities
  * removing an index column from an input table will not cause code changes;
  * adding a new index column in the input table may neither, as long as the `tkey` has value for the added column. 

```python
tkey = BuildingTabKey(id_sector=1, id_building_type=2, time_year=2030)
sectors.get_item(tkey) # -> "residential"
building_types.get_item(tkey) # -> "multiple family house"
relation_sector_building_type.get_item(tkey) # -> [1, 2]
building_stock.get_item(tkey) # -> 12000
energy_intensity_index.get_item(tkey) # -> 0.98
building_parameter_a.get_item(tkey) # -> 2
building_parameter_b.get_item(tkey) # -> 20
building_parameter_c.get_item(tkey) # -> 200
building_number.get_item(tkey) # -> 20
```

#### Collect data

Finally, users can also create an empty `tdict` by calling the `create_empty_data_tdict` function. 
The `key_cols` must be speficied. The type of the `tdict` is `Data`. 
In practice, the empty data `tdict`s can be used for collecting model results by calling the `set_item` or `accumulate_item` functions.

```python
from tab2dict import TabDict

building_number_result = TabDict.create_empty_data_tdict(key_cols=["id_sector", "id_building_type"])
tkey = BuildingTabKey(id_sector=1, id_building_type=1)
building_number_result.set_item(tkey, 10000)
tkey.id_building_type = 2
building_number_result.set_item(tkey, 20000)
building_number_result.accumulate_item(tkey, 20000)
tkey.id_building_type = 3
building_number_result.accumulate_item(tkey, 30000)


tkey.id_building_type = 1
building_number_result.get_item(tkey) # -> 10000
tkey.id_building_type = 2
building_number_result.get_item(tkey) # -> 40000
tkey.id_building_type = 3
building_number_result.get_item(tkey) # -> 30000
```


## Dependencies

* Python: 3.8 or later

| package      | user    | contributor | 
|--------------|---------|-------------|
| pandas       | &check; | &check;     |
| openpyxl     | &check; | &check;     |
| pytest       |         | &check;     |
| pytest-cov   |         | &check;     |
| black        |         | &check;     |
| pylint       |         | &check;     |

## Version History

* 04.12.2023 - Initial Release (v0.0.1)

## License

Author: [@SongminYu](https://github.com/SongminYu). 

License: MIT. 