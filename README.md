# Readme

`tab2dict` is a tool supporting data handling in developing scientific software (i.e., models). 
The tool can convert predefined input tables (`.xlsx` or `.csv`) into `TabDict` instances.
Then, the items therein can be fetched by `TabKey` instances.

There are two advantages of using `tab2dict`:
* It allows the users to adapt the input tables relatively freely (e.g., adding or removing index columns) without making many changes in the code.
* As the tables are converted to dictionaries, the fetching speed is faster, especially compared with filtering pandas dataframes. The readability is also better.

## Getting started

As a light tool, most functions of `tab2dict` are clearly shown in the test files. 
Below is a quick introduction of the main points.

### TabDict

There are three types of predefined input tables that can be converted:

* "ID" tables named as "ID_XXX"
* "Relation" tables named as "Relation_XXX"
* "Data" tables named as "Data_XXX"

In each type of tables, the column names must follow the convention shown in the example below:

First, "ID" tables, for example, the `ID_Position` and `ID_ProjectType` tables:
* The name of the first column must be `id_position` or `id_project_type`.
* The name of the second column must be `name`.

| id_position | name            |
|-------------|-----------------|
| 1           | Full Prof.      |
| 2           | Associate Prof. |
| 3           | Assistant Prof. |

| id_project_type | name    |
|-----------------|---------|
| 1               | Type A  |
| 2               | Type B  |
| 3               | Type C  |

Second, "Relation" tables, for example, the `Relation_Position_ProjectType` table:
* There can only be two columns, showing the relation between the two indexes.

| id_position | id_project_type |
|-------------|-----------------|
| 1           | 1               |
| 1           | 2               |
| 1           | 3               |
| 2           | 2               |
| 2           | 3               |
| 3           | 3               |

Third, "Data" tables, for example, the `Data_ProjectSize` table:
* There can be multiple index columns. 
* For timeseries input, besides the `id_` index columns, `tab2dict` also has `period` as a usable index column name.
* The `unit` column is optional.
* The name of the last column must be `value`.

| id_position | id_project_type | unit  | value | 
|-------------|-----------------|-------|-------|
| 1           | 1               | Euros | 300   |
| 1           | 2               | Euros | 200   |
| 1           | 3               | Euros | 100   |
| 2           | 2               | Euros | 150   |
| 2           | 3               | Euros | 80    |
| 3           | 3               | Euros | 50    |


### TabKey

`tab2dict` provides the base class `TabKey` that has to be inherited and extended according to the input table columns. 

```python
from tab2dict import TabKey

class TestTabKey(TabKey):
    def __init__(
        self,
        id_position: Optional[int] = None,
        id_project_type: Optional[int] = None,
    ):
        self.id_position = id_position
        self.id_project_type = id_project_type
```

As shown, the attributes of the `TestTabKey` class are same with the column names in the input tables. 
They must always start with `id_` (or `period`) as shown above.

### Example

```python
from tab2dict import TabDict

positions = TabDict.from_path("ID_Position.xlsx")
project_types = TabDict.from_path("ID_ProjectType.xlsx")
relation_position_project_type = TabDict.from_path("Relation_Position_ProjectType.xlsx")
project_size = TabDict.from_path("Data_ProjectSize.xlsx")
tkey = TestTabKey(id_position=1, id_project_type=2)

positions.get_item(tkey) # -> "Full Prof."
project_types.get_item(tkey) # -> "Type B"
relation_position_project_type.get_item(tkey) # -> [1, 2, 3]
project_size.get_item(tkey) # -> 200
```

In summary,

* When converting a table to a `TabDict` instance (`tdict`), the index columns are automatically identified and recorded as its `key_cols`. 
* Users can use `TabKey` instances (`tkey`) to fetch data from the dict, as long as the `tkey` knows the values of the `tdict`'s `key_cols`.
* The `tkey` can know more than necessary, which means
  * removing an index column from an input table will not cause code changes;
  * adding a new index column in the input table may neither, as long as the `tkey` knows the added column. 

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