### 1. Prepair database:
#### 1.1. Create supper user:
```angular2html
create user flyte with password ‘123456’ SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN REPLICATION;
```
#### 1.2. Create database:
```angular2html
create database flytedb;
```
#### 1.3. Grant owner for database:
```angular2html
alter database flytedb owner to flyte;
```
#### 1.4 Switch database:
```angular2html
\connect flytedb;
```
#### 1.5. Create table:
```angular2html
create table account (
username varchar(50) unique not null,
email varchar(255) not null
);
```
#### 1.6. Insert data to table:
```angular2html
insert into account values ('van', 'van@gmail.com');
```
### 2. Example workflow
#### 2.1. select 
```angular2html
from flytekit import kwtypes, task, workflow
from flytekit.types.schema import FlyteSchema
from flytekitplugins.sqlalchemy import SQLAlchemyConfig, SQLAlchemyTask
import pandas as pd

DataSchema=FlyteSchema[kwtypes(username=str, email=str)]
sql_task = SQLAlchemyTask(
    name="flyte",
    query_template="select username, email from account",
    output_schema_type=DataSchema,
    task_config=SQLAlchemyConfig(uri="postgresql://flyte:123456@localhost:30089/flytedb"),
)

@task
def get_data(data: DataSchema) -> pd.Series:
    dataframe = data.open().all()
    print(type(dataframe['email']))
    return dataframe['email']

@workflow
def my_wf() -> pd.Series:
     return get_data(data=sql_task())

if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(my_wf())
```

#### 2.1. insert
```angular2html
from flytekit import workflow
from flytekitplugins.sqlalchemy import SQLAlchemyConfig, SQLAlchemyTask

sql_task = SQLAlchemyTask(
    name="flyte",
    query_template="insert into account values ('oliver2', 'oliver2@gmail.com')",
    output_schema_type=None,
    task_config=SQLAlchemyConfig(uri="postgresql://flyte:123456@localhost:30089/flytedb"),
)


@workflow
def my_wf() -> None:
     return sql_task()

if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(my_wf())
```