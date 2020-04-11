from datetime import datetime
import sqlite3
import os


class CovidmiRepo:

    def __init__(self):
        self.DATA_PATH = os.path.join(os.path.abspath('./data'), "covid-mi.db")
        self.table_name = 'covidmi'
        self.conn = sqlite3.connect(self.DATA_PATH)
        self.cursor = self.conn.cursor()
        self.today = datetime.utcnow().strftime('%Y-%m-%d')

        self.create_table()

    def create_table(self):
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            Id INTEGER PRIMARY KEY,
            County TEXT NOT NULL,
            Cases INTEGER DEFAULT 0,
            Deaths INTEGER DEFAULT 0,
            CreatedAt TEXT
        );"""

        self.cursor.execute(create_sql)

    def insert(self, data):
        sql = f'''INSERT INTO {self.table_name} (County, Cases, Deaths, CreatedAt)
        VALUES (?,?,?,datetime('now'))'''

        self.cursor.execute(sql, data)
        self.conn.commit()

    def exists_for_today(self, county):

        sql = f"""
        SELECT COUNT(*)
        FROM {self.table_name}
        WHERE
        {self.table_name}.County = '{county}'
        AND date({self.table_name}.CreatedAt, 'localtime') = '{self.today}'
        """

        self.cursor.execute(sql)
        r = self.cursor.fetchone()

        if (r[0] == 0):
            return False
        return True

    def to_obj(self, db_result):
        return {
            'id': db_result[0],
            'county': db_result[1],
            'cases': db_result[2],
            'deaths': db_result[3],
            'createdAt': db_result[4]
        }

    def to_obj_set(self, db_result_set):
        obj_result = []

        for result in db_result_set:
            obj = self.to_obj(result)
            obj_result.append(obj)

        return obj_result

    def get_all(self):
        sql = f"""
        SELECT
            {self.table_name}.Id,
            {self.table_name}.County,
            {self.table_name}.Cases,
            {self.table_name}.Deaths,
            datetime({self.table_name}.CreatedAt, 'localtime') AS [CreatedAt]
        FROM
            {self.table_name}
        ORDER BY
            {self.table_name}.CreatedAt DESC"""

        print(sql)

        self.cursor.execute(sql)
        result_set = self.cursor.fetchall()

        return self.to_obj_set(result_set)

    def get_all_latest(self):
        sql = f"""
        SELECT
            {self.table_name}.Id,
            {self.table_name}.County,
            {self.table_name}.Cases,
            {self.table_name}.Deaths,
            datetime({self.table_name}.CreatedAt, 'localtime') AS [CreatedAt]
        FROM
            {self.table_name}
        WHERE
            date({self.table_name}.CreatedAt, 'localtime') = '{self.today}'
        ORDER BY
            {self.table_name}.CreatedAt DESC"""

        print(sql)

        self.cursor.execute(sql)
        result_set = self.cursor.fetchall()

        return self.to_obj_set(result_set)

    def get_by_county(self, county):
        sql = f"""
        SELECT
            {self.table_name}.Id,
            {self.table_name}.County,
            {self.table_name}.Cases,
            {self.table_name}.Deaths,
            datetime({self.table_name}.CreatedAt, 'localtime') AS [CreatedAt]
        FROM
            {self.table_name}
        WHERE
            {self.table_name}.County = '{county}' COLLATE NOCASE
        ORDER BY
            {self.table_name}.CreatedAt DESC"""

        print(sql)

        self.cursor.execute(sql)
        result_set = self.cursor.fetchall()

        return self.to_obj_set(result_set)
