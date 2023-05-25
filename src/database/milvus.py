import configparser
import csv
import datetime
import json
import logging
import random
import time
from typing import List, Dict, Any, Union
import jsonlines
import numpy as np
from pymilvus import FieldSchema, CollectionSchema, DataType, Collection, utility
import mysql.connector as mysql_connector
from myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)


########################################################################################################################
# Subsystem Classes:
#
# 1. ConnectAPI: responsible for establishing and maintaining connection with the milvus vector database.
# 2. CollectionAPI: responsible for creating and deleting collections in the milvus vector database.
# 3. VectorAPI: responsible for creating and deleting vectors in the milvus vector database.
# 4. IndexAPI: responsible for creating and deleting indexes in the milvus vector database.
# 5. PartitionAPI: responsible for creating and deleting partitions in the milvus vector database.
# 6. StatAPI: responsible for retrieving collection statistics from the milvus vector database.
# 7. SearchAPI: responsible for searching for vectors in the milvus vector database.
# 8. BatchAPI: responsible for batch inserting or deleting vectors in the milvus vector database.
# 9. TableAPI: responsible for retrieving the row count of a given table from the milvus vector database.
# 10. MonitorAPI: responsible for retrieving monitoring information from the milvus vector database.
########################################################################################################################
# 1. ConnectAPI:
class ConnectAPI:
    _state = None
    _config: configparser.ConfigParser = None
    _client = None
    _requests: List[Any] = None  # TODO: Define request convention format
    _responses: List[Any] = None  # TODO: Define response convention format

    def __init__(self, alias: str = None, user: str = None, password: str = None,
                 host: str = None, port: str = None, **kwargs):
        try:
            self._client = self.connect(alias=kwargs.get("alias", "default") if alias is None else alias,
                                        user=kwargs.get("user", "milvus") if user is None else user,
                                        password=kwargs.get("password", "developer") if password is None else password,
                                        host=kwargs.get("host", "127.0.0.1") if host is None else host,
                                        port=kwargs.get("port", "19530") if port is None else port,
                                        **kwargs)

            self._state = self
            # log.info(json.dumps(dir(self._client), indent=2))
        except Exception as e:
            log.error(e)

    def connect(self,
                alias: str = "default",
                user: str = "milvus",
                password: str = "developer",
                host: str = '127.0.0.1',
                port: str = '19530',
                **kwargs) -> utility:
        try:
            utility.connections.connect(alias=alias or kwargs.get("alias", "default"),
                                        user=user or kwargs.get("user", "milvus"),
                                        password=password or kwargs.get("password", "developer"),
                                        host=host or kwargs.get("host", "127.0.0.1"),
                                        port=port or kwargs.get("port", "19530"),
                                        **kwargs)
            return utility
        except Exception as e:
            log.error(e)
            return False

    def get_client(self) -> Any:
        try:
            return self._client
        except Exception as e:
            log.error(e)
            return None


# 2. CollectionAPI:
class CollectionAPI:
    _collections: List[Collection] = None  # format: ["collection_name", ...]

    def __init__(self, **kwargs):
        try:
            self._client = ConnectAPI(**kwargs).get_client()
            log.info(json.dumps(dir(self._client)))
            self._collections: List[Collection] = self._client.list_collections()
        except Exception as e:
            log.error(e)

    def create_collection(self,
                          collection_name: str,
                          fields: List[FieldSchema],
                          **kwargs
                          ) -> Collection:
        try:
            # check if collection already exists
            if collection_name in self._client.list_collections():
                log.info("Collection already exists.")
                return Collection(name=collection_name)
            # check if fields is None
            if fields is None:
                raise Exception("Fields must be specified when creating a new collection.")
            # create a new collection since it does not exist
            description = kwargs.get("description", "")
            segment_row_limit = kwargs.get("segment_row_limit", 1000000)
            auto_id = kwargs.get("auto_id", True)

            schema = CollectionSchema(fields=fields,
                                      description=description,
                                      segment_row_limit=segment_row_limit,
                                      auto_id=auto_id)
            return Collection(name=collection_name,
                              schema=schema,
                              **kwargs)
        except Exception as e:
            log.error(e)

    def list_collections(self) -> List[Collection] or None:
        try:
            return utility.list_collections()
        except Exception as e:
            log.error(e)
            return None

    def set_collections(self, collections: List[Collection]):
        try:
            self._collections.extend(collections)
        except Exception as e:
            log.error(e)
            pass

    def has_collection(self, collection_name: str) -> bool:
        if utility.has_collection(collection_name):
            return True
        else:
            return False

    def drop_collection(self, collection_name: str) -> Dict:
        try:
            if self.has_collection(collection_name):
                utility.drop_collection(collection_name)
                if not self.has_collection(collection_name):
                    return {"message": "Collection dropped.", "status": "success"}
                else:
                    return {"message": "Collection still exists.", "status": "failed"}
            else:
                return {"message": "Collection does not exist.", "status": "failed"}
        except Exception as e:
            log.error(e)
            return {"message": "Collection drop failed.", "status": "failed"}


# 3.0 EmbeddingsAPI:
class IEmbeddingsAPI:

    def __init__(self, *args, **kwargs):
        pass


# 3. VectorAPI:
class VectorAPI:
    def __init__(self):
        pass

    def create_vector(self, collection_name, vector):
        pass

    def delete_vector(self, collection_name, vector_id):
        pass


# 4. IndexAPI:
class IndexAPI:

    def __init__(self, *args, **kwargs):
        self._client = ConnectAPI(*args, **kwargs).get_client()

    def create_index(self, field_name: str, collection_name: str, schema: CollectionSchema, index_params: Dict = None,
                     using: str = "default", **kwards):
        try:
            index_params = index_params if index_params is not None else index_params
            collection = Collection(name=collection_name, schema=schema, using=using, **kwards)
            return collection.create_index(field_name=field_name, index_params=index_params, index_name="idx",
                                           **kwards)
        except Exception as e:
            log.error(e)


# 5. PartitionAPI:

class PartitionAPI:
    collection_name: str = None
    partition_params: Dict = None
    collection: Collection = None

    def __init__(self, **kwargs):
        self._client = ConnectAPI(**kwargs).get_client()

    def create_partition(self, collection_name, partition_params, **kwargs):
        try:
            self.collection_name = collection_name
            self.partition_params = partition_params
            self.collection = Collection(name=collection_name)
            self.collection.create_partition(partition_name=partition_params.name,
                                             **kwargs)
            return True
        except Exception as e:
            log.error(e)

    def delete_partition(self, collection_name, partition_params):
        try:
            self.collection = Collection(name=collection_name)
            self.collection.drop_partition(partition_name=partition_params.name)
            return True
        except Exception as e:
            log.error(e)


# 6. StatAPI:

class StatAPI:

    def __init__(self, collection_name: str = None, **kwargs):
        self._client = ConnectAPI(**kwargs).get_client()

    def get_collection_stats(self, collection_name: str = None):
        pass


# 7. SearchAPI:
class SearchAPI:
    def __init__(self, **kwargs):
        self._client = ConnectAPI(**kwargs).get_client()

    def search_vectors(self, collection_name, search_params):
        pass


# 8. BatchAPI:

class BatchAPI:
    collection_name = None
    vectors = None

    def __init__(self):
        pass

    def batch_insert_vectors(self, collection_name: str, partition_name: str, vectors: List = None):
        """
        batch_insert_vectors is a wrapper for Milvus.do_bulk_insert, inserts entities through a list of entities,
        or list of files.

        The entities must be a list of dict, and the dict must be in the format of a schema (the datastructure of the
        dataset) and dataset (the list of entities to be inserted):

        - schema: {"name": "value", "type": "value", "values": [value, value, value, ...]}
        - dataset: {"name": "xxx", "type": "binary", "values": [xxx, xxx, xxx, ...]}

        The "name" is the field name, the "values" is the field values. The "type" is the field type,
        it can be "int64", "float", "binary". For example:

        - schema: {"name": "id", "type": "int64", "values": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]},
        - dataset: {"name": "vec", "type": "float", "values": [0.190, 0.046, 0.143, 0.972, 0.592, 0.238, 0.266, 0.995, 0.064, 0.063]
                                                    [0.149, 0.586, 0.012, 0.673, 0.588, 0.917, 0.949, 0.944, 0.89, 0.028], ...]}

        - schema:  {"name": "id", "type": "int64", "values": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]},
        - dataset: {"name": "vec", "type": "binary", "values": [b'0.190, 0.046, 0.143, 0.972, 0.592, 0.238, 0.266, 0.995',
                                                        b'0.149, 0.586, 0.012, 0.673, 0.588, 0.917, 0.949, 0.944', ...]}

        inserts entities through files, currently supports row-based json file.
            User need to create the json file with a specified json format which is described in the official
            user guide. Let's say a collection has two fields: "id" and "vec"(dimension=8), the row-based json format is:
        - {"rows": [
             {"id": "0", "vec": [0.190, 0.046, 0.143, 0.972, 0.592, 0.238, 0.266, 0.995]},
             {"id": "1", "vec": [0.149, 0.586, 0.012, 0.673, 0.588, 0.917, 0.949, 0.944]}, ......
            ]
          }

        :param collection_name: collection name
        :param partition_name: partition name
        :param vectors: a list of entities/ a list of files
        :return: None
        """
        pass


# 9. TableAPI:

class TableAPI:
    def __init__(self):
        pass

    def get_table_row_count(self, table_name):
        pass


# 10. MonitorAPI:

class MonitorAPI:
    def __init__(self):
        pass

    def get_monitor_info(self):
        pass


####################################################################################################
# Additional support classes:
# 1. ConfigurationLoader: responsible for loading configuration settings from a file.
# 2. Logger: responsible for logging messages to a file.
# 3. Utils: responsible for providing utility functions such as timestamping, random number generation, etc.
# 4. ExceptionHandler: responsible for handling exceptions from the API classes.
# 5. DatabaseManager: responsible for managing the database connection and executing SQL queries.
# 6. DataLoader: responsible for loading data from external sources.
# 7. DataProcessor: responsible for pre-processing data before it is used by the API classes.
# 8. ResultProcessor: responsible for post-processing the results before they are returned to the caller.
# 9. Exporter: responsible for exporting data from the database.
# 10. Importer: responsible for importing data into the database.
####################################################################################################
# -------------------------------------------------------------------------------------------------#
# 1. ConfigurationLoader:
class ConfigurationLoader:
    def __init__(self, config_file):
        try:
            self.config_file = config_file
            self.config = None
        except Exception as e:
            log.error(e)

    def load_config(self):
        try:
            self.config = configparser.ConfigParser()
            self.config.read(self.config_file)
            return self.config
        except Exception as e:
            log.error(e)


# -------------------------------------------------------------------------------------------------#
# 2. Logger:
class Logger:
    def __init__(self):
        try:
            self.log_file = "logs/milvus.log"
            self.logger = GetLogger("milvus")
        except Exception as e:
            log.error(e)

    def create_logger(self):
        try:
            self.logger = GetLogger("milvus")
            self.logger.setLevel(logging.DEBUG)
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            return self.logger
        except Exception as e:
            log.error(e)


# -------------------------------------------------------------------------------------------------#
# 3. Utils:
class Utils:
    def __init__(self):
        pass

    def get_timestamp(self):
        return datetime.datetime().strftime("%Y-%m-%d %H:%M:%S")

    def generate_random_number(self, start: int = 0, end: int = 1000):
        return random.randint(start, end)


# -------------------------------------------------------------------------------------------------#
# 4. ExceptionHandler:
class ExceptionHandler(Exception):
    def __init__(self):
        pass

    def handle_exception(self, exception):
        log.error(exception)


# -------------------------------------------------------------------------------------------------#
# 5. DatabaseManager:
class DatabaseManager:
    config = {
        'user': 'milvus',
        'password': 'developer',
        'host': '127.0.0.1',
        'database': 'milvus_data',
        'raise_on_warnings': True
    }

    connection = None

    def __init__(self, database_config: None):
        try:
            self.config = database_config if database_config is not None and isinstance(database_config,
                                                                                        dict) else self.config
            self.connection = self.connect()
        except Exception as e:
            log.error(e)

    def connect(self):
        try:
            self.connection = mysql_connector.connect(
                host=self.config['host'],
                database=self.config['database'],
                user=self.config['user'],
                passwd=self.config['password']
            )
            return self.connection
        except Exception as e:
            log.error(e)
            raise e

    def disconnect(self):
        try:
            self.connection.disconnect()
        except Exception as e:
            log.error(e)

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor
        except Exception as e:
            log.error(e)


# -------------------------------------------------------------------------------------------------#
# 6. DataLoader:
class DataLoader:
    def __init__(self):
        pass

    def load_from_file(self, file_name):
        try:
            data = []
            with open(file_name, 'r') as f:
                for line in f:
                    data.append(line.strip())
            return data
        except Exception as e:
            log.error(e)

    def load_from_csv(self, file_name):
        try:
            data = []
            with open(file_name, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            log.error(e)

    def load_from_json(self, file_name):
        try:
            data = []
            with jsonlines.open(file_name) as reader:
                for obj in reader:
                    data.append(obj)
            return data
        except Exception as e:
            log.error(e)

    def load_from_dataframe(self, dataframe):
        try:
            data = []
            for index, row in dataframe.iterrows():
                data.append(row)
            return data
        except Exception as e:
            log.error(e)

    def load_from_dict(self, dictionary):
        try:
            data = []
            for key, value in dictionary.items():
                data.append(value)
            return data
        except Exception as e:
            log.error(e)


# -------------------------------------------------------------------------------------------------#
# 7. DataProcessor:
class DataProcessor:
    def __init__(self):
        pass

    def pre_process(self, data):
        # Process the data
        pass


# -------------------------------------------------------------------------------------------------#
# 8. ResultProcessor:
class ResultProcessor:
    def __init__(self):
        pass

    def post_process(self, results):
        # Process the results
        pass


# -------------------------------------------------------------------------------------------------#
# 9. Exporter:
class Exporter:
    def __init__(self):
        pass

    def export_to_csv(self, data, file_name):
        try:
            with open(file_name, 'w') as f:
                writer = csv.writer(f)
                for row in data:
                    writer.writerow(row)
        except Exception as e:
            log.error(e)

    def export_to_json(self, data, file_name):
        try:
            with jsonlines.open(file_name, mode='w') as writer:
                writer.write_all(data)
        except Exception as e:
            log.error(e)


# -------------------------------------------------------------------------------------------------#
# 10. Importer:
class Importer:
    def __init__(self):
        pass

    def import_from_csv(self, file_name):
        try:
            data = []
            with open(file_name, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            log.error(e)

    def inport_from_json(self, file_name):
        """get json using jsonlines package

        :param file_name: file path and name
        :return: json data
        """
        try:
            data = []
            with jsonlines.open(file_name) as reader:
                for obj in reader:
                    data.append(obj)
            return data
        except Exception as e:
            log.error(e)


# -------------------------------------------------------------------------------------------------#
# 11. DataGenerator:
class DataGenerator:

    def __init__(self):
        pass

    def generate_vectors(self, vector_type, vector_size, vector_count):
        try:
            if vector_type == 'binary':
                vectors = np.random.randint(0, 2, (vector_count, vector_size))
            elif vector_type == 'float':
                vectors = np.random.rand(vector_count, vector_size)
            elif vector_type == 'int':
                vectors = np.random.randint(0, 1000, (vector_count, vector_size))
            elif vector_type == 'string':
                vectors = np.random.randint(0, 1000, (vector_count, vector_size))
                vectors = vectors.astype(str)
            return vectors
        except Exception as e:
            log.error(e)

    def generate_ids(self, vector_count):
        try:
            ids = np.random.randint(0, 1000000, vector_count)
            return ids
        except Exception as e:
            log.error(e)

    def generate_vectors_and_ids(self, vector_type, vector_size, vector_count):
        try:
            vectors = self.generate_vectors(vector_type, vector_size, vector_count)
            ids = self.generate_ids(vector_count)
            return vectors, ids
        except Exception as e:
            log.error(e)


# -------------------------------------------------------------------------------------------------#
# Abstraction layer for Milvus API
class MilvusAPI(ConnectAPI, CollectionAPI, PartitionAPI, IndexAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

