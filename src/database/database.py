# Helper file for database operations
import sqlite3
from typing import Any, List

class Param:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

class Database:

    def __init__(self, path:str):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.conn.close()

    def execute(self, query:str, params=None):
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        self.conn.commit()

    def get_all(self, table:str) -> List[Any]:
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
        
    def get_by_id(self, table:str, id)-> List[Any]:
        query = f"SELECT * FROM {table} WHERE id=?"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()
    
    def get_by_param(self, table:str, param:Param)-> List[Any]:
        query = f"SELECT * FROM {table} WHERE {param.name}=?"
        self.cursor.execute(query, (param.value,))
        return self.cursor.fetchall()
    
    def get_by_ids(self, table:str, ids)-> List[Any]:
        query = f"SELECT * FROM {table} WHERE id IN ({','.join('?'*len(ids))})"
        self.cursor.execute(query, ids)
        return self.cursor.fetchall()
    
    def get_by_params(self, table: str, params: List[Param])-> List[Any]:
        query = f"SELECT * FROM {table} WHERE "
        for key, value in params.items():
            query += f"{key}=? AND "
        query = query[:-5] # Remove last ' AND '
        self.cursor.execute(query, tuple(params.values()))
        return self.cursor.fetchall()

    def get_join_all(self, table:str, join_table:str, table_on:str, join_table_on:str)-> List[Any]:
        query = f"SELECT * FROM {table} JOIN {join_table} ON {table}.{table_on}={join_table}.{join_table_on}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_join_all_by_id(self, table:str, join_table:str, table_on:str, join_table_on:str, id)-> List[Any]:
        query = f"SELECT * FROM {table} JOIN {join_table} ON {table}.{table_on}={join_table}.{join_table_on} WHERE {table}.id=?"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()

    def get_join_all_by_param(self, table:str, join_table:str, table_on:str, join_table_on:str, param:Param)-> List[Any]:
        query = f"SELECT * FROM {table} JOIN {join_table} ON {table}.{table_on}={join_table}.{join_table_on} WHERE {param.name}=?"
        self.cursor.execute(query, (param.value,))
        return self.cursor.fetchall()
    
    def get_join_all_by_ids(self, table:str, join_table:str, table_on:str, join_table_on:str, ids)-> List[Any]:
        query = f"SELECT * FROM {table} JOIN {join_table} ON {table}.{table_on}={join_table}.{join_table_on} WHERE {table}.id IN ({','.join('?'*len(ids))})"
        self.cursor.execute(query, ids)
        return self.cursor.fetchall()
    
    def get_join_all_by_params(self, table:str, join_table:str, table_on:str, join_table_on:str, params:List[Param])-> List[Any]:
        query = f"SELECT * FROM {table} JOIN {join_table} ON {table}.{table_on}={join_table}.{join_table_on} WHERE "
        for param in params:
            query += f"{param.name}=? AND "
        query = query[:-5]
        self.cursor.execute(query, tuple([param.value for param in params]))
        return self.cursor.fetchall()

    def get_foreign_key(self, table:str, foreign_key:str, id)-> List[Any]:
        query = f"SELECT * FROM {table} WHERE {foreign_key}=?"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()

    def get_foreign_keys(self, table:str, foreign_key:str, ids)-> List[Any]:
        query = f"SELECT * FROM {table} WHERE {foreign_key} IN ({','.join('?'*len(ids))})"
        self.cursor.execute(query, ids)
        return self.cursor.fetchall()
    
    def n_join_by_params(self, tables:List[str], table_ons:List[str], params:List[Param] = None, select=None)-> List[Any]:
        query = f"SELECT {'*' if select is None else f'{select}.*'} FROM {tables[0]} "
        for i in range(len(tables)-1):
            query += f"JOIN {tables[i+1]} ON {tables[i]}.{table_ons[i][0]}={tables[i+1]}.{table_ons[i][1]} "
        if params is not None:
            query += "WHERE "
            for param in params:
                query += f"{param.name}=? AND "
            query = query[:-5]
        self.cursor.execute(query, tuple([param.value for param in params]))
        return self.cursor.fetchall()