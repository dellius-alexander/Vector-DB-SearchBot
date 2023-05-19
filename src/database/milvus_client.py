from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
import sys
import os
from myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)
LOGGER = log.logger


MILVUS_HOST = os.getenv("MILVUS_HOST", "127.0.0.1")
# MILVUS_HOST = os.getenv("MILVUS_HOST", "192.168.1.85")
MILVUS_PORT = int(os.getenv("MILVUS_PORT", "19530"))
VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", "768"))
INDEX_FILE_SIZE = int(os.getenv("INDEX_FILE_SIZE", "1024"))
METRIC_TYPE = os.getenv("METRIC_TYPE", "IP")
DEFAULT_TABLE = os.getenv("DEFAULT_TABLE", "milvus_qa_search_1")
TOP_K = int(os.getenv("TOP_K", "10"))


class Milvus:
    """
    Milvus is a Python wrapper for the pymilvus library, providing an
    easy-to-use interface for performing basic operations such as
    connecting to Milvus, creating collections, and inserting/querying vectors.
    """

    def __init__(self) -> None:
        try:
            self.collection = None
            connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
            LOGGER.debug(f"Successfully connect to Milvus with IP:{MILVUS_HOST,} and PORT:{MILVUS_PORT}")
        except Exception as e:
            LOGGER.error(f"Failed to connect Milvus: {e}")
            sys.exit(1)

    def set_collection(self, collection_name: str, schema: CollectionSchema, **kwargs) -> None:
        try:
            if self.has_collection(collection_name):
                self.collection = Collection(name=collection_name, schema=schema, **kwargs)
            else:
                raise Exception(f"There has no collection named:{collection_name}")
        except Exception as e:
            LOGGER.error(f"Error: {e}")
            sys.exit(1)

    def has_collection(self, collection_name: str) -> bool:
        # Return if Milvus has the collection
        try:
            status = utility.has_collection(collection_name=collection_name)
            print("Has collection: %s" % status)
            return status
        except Exception as e:
            LOGGER.error(f"Failed to check collection: {e}")
            sys.exit(1)

    def create_collection(self, collection_name: str, fields: list = None, **kwargs) -> str:
        # Create milvus collection if not exists
        try:
            if not self.has_collection(collection_name):
                schema = CollectionSchema(fields=[fields], description="collection description", **kwargs)
                self.collection = Collection(name=collection_name, schema=schema, **kwargs)
                LOGGER.debug(f"Create Milvus collection: {self.collection}")
            return "OK"
        except Exception as e:
            LOGGER.error(f"Failed to create collection: {e}")
            sys.exit(1)

    def insert(self, collection_name: str, vectors: list) -> list:
        # Batch insert vectors to milvus collection
        try:
            if not self.has_collection(collection_name):
                raise Exception(f"There has no collection named:{collection_name}")
            collection = Collection(name=collection_name)
            data = [vectors]
            collection.insert(data=data)
            LOGGER.debug(f"Insert vectors to Milvus in collection: {collection_name} with {len(vectors)} rows")
            return True
        except Exception as e:
            LOGGER.error(f"Failed to insert data into Milvus: {e}")
            sys.exit(1)

    def create_index(self, collection_name: str) -> str:
        # Create IVF_FLAT index on milvus collection
        try:
            if not self.has_collection(collection_name):
                raise Exception(f"There has no collection named:{collection_name}")
            self.set_collection(collection_name)
            default_index = {"index_type": "IVF_SQ8", "metric_type": METRIC_TYPE, "params": {"nlist": 16384}}
            status = self.collection.create_index(field_name="embedding", index_params=default_index)
            if not status.code:
                LOGGER.debug(
                    f"Successfully create index in collection:{collection_name} with param:{default_index}")
                return status
            else:
                raise Exception(status.message)
        except Exception as e:
            LOGGER.error(f"Failed to create index: {e}")
            sys.exit(1)

    def delete_collection(self, collection_name: str) -> str:
        # Delete Milvus collection
        try:
            self.set_collection(collection_name)
            self.collection.drop()
            LOGGER.debug("Successfully drop collection!")
            return "ok"
        except Exception as e:
            LOGGER.error(f"Failed to drop collection: {e}")
            sys.exit(1)

    def search_vectors(self, collection_name: str, vectors: list, top_k: int) -> list:
        # Search vector in milvus collection
        try:
            if not self.has_collection(collection_name):
                raise Exception(f"There has no collection named:{collection_name}")
            collection = Collection(name=collection_name)
            search_params = {"metric_type": METRIC_TYPE, "params": {"nprobe": 16}}
            response = collection.search(vectors, anns_field="embedding", param=search_params, limit=top_k)
            LOGGER.debug(f"Successfully search in collection: {response}")
            return response
        except Exception as e:
            LOGGER.error(f"Failed to search in Milvus: {e}")
            sys.exit(1)

    def count(self, collection_name: str) -> int:
        # Get the number of milvus collection
        try:
            self.set_collection(collection_name)
            num = self.collection.num_entities
            LOGGER.debug(f"Successfully get the num:{num} of the collection:{collection_name}")
            return num
        except Exception as e:
            LOGGER.error(f"Failed to count vectors in Milvus: {e}")
            sys.exit(1)

    def get_collection(self,
                       collection_name: str,
                       fields: list,
                       segment_row_limit: int = 100,
                       using: str = 'default',
                       **kwargs) -> Collection:
        """
        Creates a new Collection object

        Arguments:
            collection_name {str} -- [Name of the collection]
            fields {list} -- [Fields of the collection]
            segment_row_limit {int} -- [Max number of rows per segment]

        Keyword Arguments:
            using {str} -- [The database to use] (default: {'default'})

        Returns:
            Collection -- [Collection Object]
        """
        return Collection(name=collection_name, fields=fields, segment_row_limit=segment_row_limit, using=using,
                          **kwargs)

    def get_collection_schema(self,
                              collection_name: str,
                              fields: list,
                              segment_row_limit: int = 100) -> CollectionSchema:
        """
        Creates a new CollectionSchema object

        Arguments:
            collection_name {str} -- [Name of the collection]
            fields {list} -- [Fields of the collection]
            segment_row_limit {int} -- [Max number of rows per segment]

        Returns:
            CollectionSchema -- [Collection Schema Object]
        """
        return CollectionSchema(
            collection_name=collection_name,
            fields=fields,
            segment_row_limit=segment_row_limit,
        )
