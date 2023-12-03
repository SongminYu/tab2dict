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
They must always start with `id_`, also as shown above. 
Furthermore, to include timeseries table, `tab2dict` also has `period` as a default column name.

## Dependencies

-   Python 3.8+
-   pytest
-   pytest-cov
-   pylint
-   black

## Version History

-   0.0.1
    -   Initial Release

## License

Author: [@SongminYu](https://github.com/SongminYu). 

License: MIT. 