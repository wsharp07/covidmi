from datetime import datetime
import pyodbc
import os


class CovidmiRepo:

    def __init__(self):
        self.connection = pyodbc.connect(self.get_conn_string())
        self.cursor = self.connection.cursor()
        self.table_name = 'covidmi'
        self.TIMEZONE = 'Eastern Standard Time'
        self.today = datetime.utcnow().strftime('%Y-%m-%d')

        self.create_table()

    def get_conn_string(self):
        server = os.getenv('SQL_HOSTNAME')
        database = os.getenv('SQL_DATABASE')
        username = os.getenv('SQL_USERNAME')
        password = os.getenv('SQL_PASSWORD')
        return "DRIVER={ODBC Driver 17 for SQL Server};" + \
            f"SERVER={server};" + \
            f"DATABASE={database};" + \
            f"UID={username};" + \
            f"PWD={password}"

    def create_table(self):
        create_sql = f"""
        IF NOT EXISTS (SELECT * FROM sysobjects
        WHERE name='{self.table_name}' and xtype='U')
            CREATE TABLE {self.table_name} (
                Id INT PRIMARY KEY IDENTITY,
                County VARCHAR(50) NOT NULL,
                Cases INT DEFAULT 0,
                Deaths INT DEFAULT 0,
                CreatedAt DATETIME DEFAULT GETUTCDATE()
            );
        """
        print(create_sql)
        self.cursor.execute(create_sql)
        self.connection.commit()

    def insert(self, data):
        sql = f'''INSERT INTO {self.table_name} (County, Cases, Deaths)
        VALUES (?,?,?)'''

        self.cursor.execute(sql, data)
        self.connection.commit()

    def exists_for_today(self, county):

        sql = f"""
        SELECT
            COUNT(*)
        FROM
            {self.table_name}
        WHERE
            {self.table_name}.County = '{county}'
            AND CAST({self.table_name}.CreatedAt
                    AT TIME ZONE 'UTC'
                    AT TIME ZONE '{self.TIMEZONE}' AS DATE) = '{self.today}'
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
            CAST({self.table_name}.CreatedAt
                AT TIME ZONE 'UTC'
                AT TIME ZONE '{self.TIMEZONE}' AS NVARCHAR) AS [CreatedAt]
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
            CAST({self.table_name}.CreatedAt
                AT TIME ZONE 'UTC'
                AT TIME ZONE '{self.TIMEZONE}' AS NVARCHAR) AS [CreatedAt]
        FROM
            {self.table_name}
        WHERE
            CAST({self.table_name}.CreatedAt
                AT TIME ZONE 'UTC'
                AT TIME ZONE '{self.TIMEZONE}' AS DATE) = '{self.today}'
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
            CAST({self.table_name}.CreatedAt
                AT TIME ZONE 'UTC'
                AT TIME ZONE '{self.TIMEZONE}' AS NVARCHAR) AS [CreatedAt]
        FROM
            {self.table_name}
        WHERE
            {self.table_name}.County = '{county}'
        ORDER BY
            {self.table_name}.CreatedAt DESC"""

        print(sql)

        self.cursor.execute(sql)
        result_set = self.cursor.fetchall()

        return self.to_obj_set(result_set)
