import traceback
from dataclasses import dataclass
from typing import List, Dict, Any
from pandas import DataFrame
from pymilvus import connections as milvus_connection, CollectionSchema, FieldSchema, Collection

from database.milvus import MilvusAPI
from myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)


class IMilvus:
    pass


@dataclass
class QAData:
    question: str
    answer: str
    ids: List[Any]
    question_data: List[Any]
    answer_data: List[Any]
    data: DataFrame
    collection_name: str


@dataclass
class Milvus(IMilvus):
    milvus_connection: milvus_connection
    collection: Collection
    collection_name: str
    collection_schema: CollectionSchema
    table_name: str
    search_param: dict
    search_params: dict
    query_vec: list
    embed: Any
    query_embeddings: list
    results: list
    status: list


class MilvusClient:
    milvus_connection: milvus_connection
    collection: Collection
    collection_name: str
    collection_schema: CollectionSchema
    table_name: str
    search_param: dict
    search_params: dict
    query_vec: list
    embed: Any
    query_embeddings: list
    results: list
    status: list

    def __init__(self, **kwargs):
        self.client = MilvusAPI(**kwargs)
        self.collection = None

    def create_collection(self, table_name, fields: List[FieldSchema], **kwargs):
        try:
            collection = None if self.collection is None else self.collection
            field_name = kwargs.get('field_name', 'embedding')
            log.info(f"Has collection {table_name}: {self.client.has_collection(table_name)}")
            if not self.client.has_collection(table_name):
                collection = self.client.create_collection(collection_name=table_name,
                                                           fields=fields, )
                index_params = {
                    "index_type": "IVF_FLAT",
                    "metric_type": "IP",
                    "params": {"nlist": 200}
                }

                self.client.create_index(
                    field_name=field_name,
                    collection_name=collection.name,
                    schema=collection.schema,
                    index_params=index_params
                )
                log.info(f"Collection \"{table_name}\" created successfully!")
            else:
                collection = Collection(name=table_name)
                log.info(f"Collection \"{table_name}\" already exists!")
            return collection
        except Exception as e:
            log.error(f"Error while creating collection: {e}")
            log.error(traceback.format_exc())
            raise e

    def store_embeddings(self, sentence_embeddings) -> list or None:
        """
        Stores embeddings in Milvus

        :param sentence_embeddings: sentence embedding
        :return: ids of the stored embeddings
        """
        try:
            mr = self.client.collection.insert([sentence_embeddings])
            log.info("Embeddings stored successfully!")
            return mr.primary_keys  # ids of the stored embeddings
        except Exception as e:
            log.error(f"Error while storing embeddings: \nClient: {self.client}\n{e}")
            log.error(traceback.format_exc())
            raise e

    def search_in_milvus(self, query_embeddings):
        try:
            search_params = {"metric_type": 'IP', "params": {"nprobe": 16}}
            log.info("Partitions: {}".format(self.client.collection.partitions))
            # Load collection
            self.client.collection.load()
            # Search
            results = self.client.collection.search(
                query_embeddings,
                anns_field=self.collection_schema.field_name,
                param=search_params,
                limit=5
            )
            log.info("Milvus searches data successfully")
            log.info("Search results: {}".format(len(results)))
            return results
        except Exception as e:
            log.error(f"Error while searching in Milvus: \nClient: {self.client} \n{e}")
            log.error(traceback.format_exc())
            raise e
