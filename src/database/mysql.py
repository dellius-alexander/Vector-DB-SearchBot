import traceback
from dataclasses import dataclass
from typing import List, Any

from pymysql import connections as mysql_connection
import pymysql
from myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)


@dataclass
class Mysql:
    host: str
    port: int
    user: str
    password: str
    database: str
    connection: mysql_connection
    cursor: Any
    sql: str


class MySQLDatabase(Mysql):
    def __init__(self, host, port, user, password, database, **kwargs):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.connect(host, port, user, password, database, **kwargs)
        self.cursor = self.connection.cursor()

    def connect(self, host, port, user, password, database, **kwargs) -> mysql_connection:
        try:

            charset = kwargs.get('charset', 'utf8mb4')
            host = host if host else self.host
            port = port if port else self.port
            user = user if user else self.user
            password = password if password else self.password
            database = database if database else self.database
            connection = pymysql.connect(host=host,
                                         port=port,
                                         user=user,
                                         password=password,
                                         db=database,
                                         charset=charset,
                                         )
            return connection
        except Exception as e:
            log.error(f'Error while connecting to Milvus and MySQL: {e}')
            log.error(traceback.format_exc())
            raise e

    def execute_batch_query(self, queries):
        try:
            with self.connection.cursor() as cursor:
                for query in queries:
                    cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            log.error(f'Error while executing batch query: \n{queries} \n{e}')
            log.error(traceback.format_exc())
            self.connection.rollback()
            raise e
        finally:
            cursor.close()

    def execute_query(self, query, args=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, args)
            self.connection.commit()
        except Exception as e:
            log.error(f'Error while executing query: \n{query} \n{e}')
            log.error(traceback.format_exc())
            self.connection.rollback()
            raise e
        finally:
            cursor.close()

    def query(self, query, args=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, args)
                result = cursor.fetchall()
            self.connection.commit()
        except Exception as e:
            log.error(f'Error while executing query: \n{query} \n{e}')
            log.error(traceback.format_exc())
            self.connection.rollback()
            raise e
        finally:
            cursor.close()
        return result

    def insert(self, query: str, args=None):
        try:
            # validate query
            if "insert" not in query.split(" "):
                raise ValueError("Query must be an insert query")
            return self.execute_query(query, args)
        except Exception as e:
            log.error(f'Error while executing insert query: \n{query} \n{e}')
            log.error(traceback.format_exc())
            self.connection.rollback()
            raise e

    def update(self, query, args):
        """
        Updates data in MySQL

        :param query: query to be executed
        :param args: arguments to be passed to the query
        :return: None
        """
        try:
            # validate query
            if "update" not in query.split(" "):
                raise ValueError("Query must be an update query")
            return self.execute_query(query, args)
        except Exception as e:
            log.error(f'Error while executing update query: \n{query} \n{e}')
            log.error(traceback.format_exc())
            self.connection.rollback()
            raise e

    def delete(self, query, args):
        """
        Deletes data from MySQL

        :param query: query to be executed
        :param args: arguments to be passed to the query
        :return: None
        """
        try:
            # validate query
            if "delete" not in query.split(" "):
                raise ValueError("Query must be a delete query")
            return self.execute_query(query, args)
        except Exception as e:
            log.error(f'Error while executing delete query: \n{query} \n{e}')
            log.error(traceback.format_exc())
            self.connection.rollback()
            raise e

    def load_data_to_mysql(self, table_name, data) -> None:
        """
        Loads data into MySQL

        :param table_name: name of the table
        :param data: data to be loaded
        :return: None
        """
        sql = "insert into " + table_name + " (id, question, answer) values (%s, %s, %s);"
        # check if the data to be inserted is already present
        check_sql = f"SELECT COUNT(*) FROM {table_name} WHERE id = %s"
        try:
            cnt = 0
            for row in data:
                with self.connection.cursor() as cursor:
                    cursor.execute(check_sql, (row[0],))
                    result = cursor.fetchone()[0]
                    if result == 0:
                        cursor.execute(sql, row)
                        self.connection.commit()
                        cnt += 1
                        if cnt == 0:
                            log.info("MYSQL loads data to table: {} successfully".format(table_name))
            log.info("MYSQL loads data to table: {} successfully. Number of Records: {}".format(table_name, cnt))
        except Exception as e:
            log.error(f'Error while loading data to MySQL. Sql insert error: \n{sql}\n{e} ')
            log.error(traceback.format_exc())
            raise e

    def get_similar_questions(self, ids, table_name) -> List:
        """
        Gets the similar questions from MySQL

        :param ids: ids of the similar questions
        :param table_name: name of the table
        :return: list of similar questions
        """
        str_ids = str(ids).replace('[', '').replace(']', '')
        sql = "select question from " + table_name + " where id in (" + str_ids + ") order by field (id," + str_ids + ");"
        try:
            if ids is None or len(ids) == 0:
                return []
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                results = [res[0] for res in results]
                return results
        except Exception as e:
            log.error(f'Error while getting similar questions: \nSql: \n{sql} \n{e} ')
            log.error(traceback.format_exc())
            raise e

    def search_by_similar_questions(self, table_name, question=None) -> List:
        """
        Searches for the answer by similar questions

        :param question: question
        :param table_name: name of the table
        :return: answer list
        """
        sql = "select answer from " + table_name + " where question = `None`;"
        try:
            if question is None or len(question) == 0:
                raise Exception("Question is None or empty")
            sql = "select answer from " + table_name + " where question in ('" + question[0] + "');"
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                if rows is None or len(rows) == 0:
                    raise Exception("No answer found")
                return rows
        except Exception as e:
            log.error(f'Error while searching by similar questions: \nSql: \n{sql} \n{e} ')
            log.error(traceback.format_exc())
            return []

