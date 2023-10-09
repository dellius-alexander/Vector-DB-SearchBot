# %%px --process-after=0
import asyncio
import concurrent
import multiprocessing.pool
import os
import time
import traceback
# from types import NoneType
from typing import List, Any, Dict, Tuple
import numpy as np
import pymysql
from pandas import DataFrame
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility, SearchResult
from sentence_transformers import SentenceTransformer
from difflib import Differ
from sklearn.preprocessing import normalize
from torch._C import NoneType

from src.myLogger.Logger import getLogger as GetLogger
from src.config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, \
    MILVUS_HOST, MILVUS_PORT, MILVUS_USER, MILVUS_PASSWORD, MILVUS_COLLECTION, \
    MYSQL_DATABASE_TABLE_NAME, MILVUS_CONNECTION_ALIAS, DATASET_PATH, MODEL_SELECTION

log = GetLogger(__name__)


def batch_retrival(arr, batch_amount) -> List:
    """
    Retrieves the batch amount from the array until the end of the array is reached
    
    :param arr: array
    :param batch_amount: batch amount to retrieve each loop
    """

    batch_index = 0  # initial starting index
    log.info(f'batch_retrival: {len(arr)}')
    while (batch_index + batch_amount) <= len(arr):  # if index plus batch amount is not greater than array length
        yield np.array(arr[batch_index:batch_index + batch_amount])  # yield portion of array
        batch_index += (batch_amount - 1)  # add batch amount to index
    # output rest of array if the length of the array is not a multiple of batch_amount
    if batch_index < len(arr):
        yield np.array(arr[batch_index:])


# Setting up milvus and mysql connection
def connect_to_milvus_and_mysql():
    """
    Connects to Milvus and MySQL
    """
    try:
        connections.connect(alias=MILVUS_CONNECTION_ALIAS,
                            user=MILVUS_USER,
                            password=MILVUS_PASSWORD,
                            host=MILVUS_HOST,
                            port=int(MILVUS_PORT))

        conn = pymysql.connect(host=MYSQL_HOST,
                               port=int(MYSQL_PORT),
                               user=MYSQL_USER,
                               password=MYSQL_PASSWORD,
                               database=MYSQL_DATABASE,
                               local_infile=True)
        cursor = conn.cursor()
        log.debug(f'Connection with {MYSQL_DATABASE} found {connections.has_connection(alias=MILVUS_CONNECTION_ALIAS)}')
        return conn, cursor, Collection(name=MYSQL_DATABASE_TABLE_NAME)
    except Exception as e:
        log.error(f'Error while connecting to Milvus and MySQL: {e}')
        log.error(traceback.format_exc())
        raise e


# Creating Collection and Setting Index
def create_collection(table_name) -> Collection:
    """
    Creates a collection in Milvus

    :param table_name: name of the collection
    :return: collection object
    """
    try:
        # Deleting previouslny stored table for clean run
        if not utility.has_collection(table_name):
            # utility.drop_collection(table_name)
            _fields = [
                FieldSchema(name="id", dtype=DataType.INT64, descrition="int64", is_primary=True, auto_id=True),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, descrition="float vector", dim=768,
                            is_primary=False)
            ]
            _schema = CollectionSchema(fields=_fields, description=f"{table_name} collection")
            __collection = Collection(name=table_name, schema=_schema)

            _index_params = {"index_type": "IVF_FLAT", "metric_type": 'IP', "params": {"nlist": 200}}
            __collection.create_index(field_name="embedding", index_params=_index_params)
            log.info(f"Collection \"{__collection.name}\" created successfully!")
            return __collection
        else:
            log.info(f"Collection \"{table_name}\" already exists!")
            return Collection(name=table_name)
    except Exception as e:
        log.error(f'Error while creating collection: {e}')
        log.error(traceback.format_exc())
        raise e


# Creating Table in MySQL
def create_table_in_mysql(cursor, table_name) -> None:
    """
    Creates a table in MySQL

    :param cursor: cursor object
    :param table_name: name of the table
    :return: None
    """
    sql = "CREATE TABLE if not exists " + table_name + " (id TEXT, question TEXT, answer TEXT);"
    try:
        # checks if the table exists in the database
        check_table = "SHOW TABLES LIKE '" + table_name + "'"
        cursor.execute(check_table)
        exists = cursor.fetchone()
        # if the table does not exist, create it
        if not exists:
            cursor.execute(sql)
            log.info(f"The {table_name} table was successfully created!")
        else:
            log.info(f"The {table_name} table already exists!")
    except Exception as e:
        log.error(f'Error while creating table in MySQL: \n{e}')
        log.error(traceback.format_exc())
        raise e


def store_embeddings(collection, sentence_embeddings) -> List[Any] or None:
    """
    Stores embeddings in Milvus

    :param collection: collection object
    :param sentence_embeddings: sentence embedding
    :return: ids of the stored embeddings
    """
    try:
        collection.load()
        if collection.num_entities != len(sentence_embeddings):
            log.info(f"Number of entities in collection: {collection.num_entities}")
            log.info(f"Number of embeddings: {len(sentence_embeddings)}")
            # Validate if the embedding exist before inserting
            mr = collection.insert([sentence_embeddings])
            log.info("Embeddings stored successfully!")
            return mr.primary_keys  # ids of the stored embeddings
    except Exception as e:
        log.error(f'Error while storing embeddings: \nCollection: {collection} \n{e}')
        log.error(traceback.format_exc())
        raise e


def generate_embeddings(data, model=None) -> Tuple[List[Any], Dict]:
    """
    Generates embeddings for the questions and answers

    :param data: data object
    :param model: sentence transformer model
    :return: sentence_embeddings
    """
    try:
        if model is None:
            model = SentenceTransformer('all-mpnet-base-v2')
        # Get questions and answers.
        question_data = data['question'].tolist()
        answer_data = data['answer'].tolist()
        # Generate embeddings
        sentence_embeddings = model.encode([data])
        log.info(f"Raw embeddings: \n{sentence_embeddings}")

        sentence_embeddings = normalize(sentence_embeddings).tolist()
        log.info(f"Normalized embeddings: \n{sentence_embeddings}")
        return sentence_embeddings
    except Exception as e:
        log.error(f'Error while generating embeddings: \nModel: {model} \n{e}')
        log.error(traceback.format_exc())
        raise e


def least_common_divisor(num):
    for i in range(1, num + 1):
        if num % i == 0:
            for divisor in range(2, i + 1):
                if (i % divisor == 0) and (num % divisor == 0):
                    return divisor


def array_split(data, batch_size) -> np.ndarray:
    """
    Splits the data into batches

    :param data: data object
    :param batch_size: size of the batch
    :return: batches of the data
    """
    arr = []
    end = batch_size
    dataset_size = len(data)
    log.debug(f"Dataset size: {dataset_size}")
    for start in range(0, dataset_size, batch_size):
        log.debug(f"\nStart: {start} End: {end}")
        if end <= dataset_size:
            chunk = np.array(data[start:end].tolist(), dtype=object)
            size_of_batch = (end - start)
            log.debug(f"\nBatch Size: {size_of_batch} \nChunk: \n{chunk}")
            # arr.append(chunk)
            # log.debug(f"\nStart: {start} End: {end}")
            end += size_of_batch
            arr.append(chunk)
            log.debug(f"\nShape: {chunk.shape}"
                      f"\nChunk: \n{chunk.size}")
    arr = np.array(arr, dtype=object)
    log.debug(f"\nBatches Shape: {arr.shape}, \nBatches: \n{arr}")
    return arr


async def model_encoder(data: np.array = None, model=None) -> np.array:
    try:
        # log.debug(f"\nDataset: \n{data}")
        if f"{data}" == "None":
            return None
        else:
            encoded_dataset = normalize(model.encode(data))
        # log.debug(f"\nEncoded dataset: \n{encoded_dataset}")
        return encoded_dataset
    except Exception as e:
        log.error(f'\nError while encoding the dataset: {e}')
        log.error(traceback.format_exc())
        return None


async def async_model_encoder(data: np.array, model) -> np.array:
    return await model_encoder(data, model)


async def async_generate_embeddings(data: np.array, model) -> np.array:
    tasks = []
    try:
        # log.debug(f"\nDataset: {data}")
        start = time.perf_counter()
        dataset_size = len(data)
        lcd = least_common_divisor(dataset_size) \
            if least_common_divisor(dataset_size) != dataset_size \
            else least_common_divisor(dataset_size - 1)
        # negate the first digit, if Integer has one digit to produce exponent equal 0.
        exponent = len(str(dataset_size)) - 1
        divisor = lcd ** exponent
        batch_size = dataset_size // divisor
        remainder = dataset_size % divisor
        batched_data_chunks = array_split(np.array(data, dtype=object), batch_size)
        batched_data_chunks_size = len(batched_data_chunks)
        log.info(f"\nDataset size: {dataset_size}"
                 f"\nBatch size: {batch_size}"
                 f"\nBatches: {batched_data_chunks_size}"
                 f"\nLeast common divisor: {lcd}"
                 f"\nExponent: {exponent}"
                 f"\nDivisors: {divisor}")
        # create tasks for each batch of data to be encoded and store them in a list
        for i in range(0, batched_data_chunks_size):
            batch = np.array(batched_data_chunks[i], dtype=object)
            if batch.size == 0:
                continue
            # log.debug(f"Batch: \n{batch}")
            task = asyncio.create_task(async_model_encoder(batch, model))
            tasks.append(task)
            # run the tasks concurrently and store the embeddings in a list
            # for task in tasks:
        log.debug("\nGenerating embeddings ...")
        sentence_embeddings = []
        for task in tasks:
            resp = await asyncio.gather(task)
            if resp[0] is None:
                continue
            sentence_embeddings.extend(resp[0].tolist())
        # sentence_embeddings = await asyncio.gather(*tasks)
        sentence_embeddings = np.array(sentence_embeddings, dtype=object)
        stop = time.perf_counter()
        embeddings_count = sentence_embeddings.size
        log.debug(f"\nTime taken to generate embeddings: {stop - start:.5f} seconds"
                  f"\nNumber of entities in dataset: {dataset_size}"
                  f"\nTotal Embeddings: {embeddings_count}, Shape: {sentence_embeddings.shape}"
                  f"\nEmbeddings Generated per Milliseconds: {(embeddings_count / (stop - start)):.5f} ms")
        return sentence_embeddings
    except Exception as e:
        log.error(f'Error while generating embeddings: \nModel: {model} \n{e}')
        # log.error(data)
        log.error(traceback.format_exc())


def encode_data(data: np.array, model) -> List[Any]:
    return asyncio.run(async_generate_embeddings(data, model))


# Processing and Storing QA Dataset
def generate_and_store_embeddings(collection: Collection,
                                  data: DataFrame, model) -> Tuple[List[Any], List[Any], List[Any]]:
    """
    Generates embeddings for the questions and answers and stores them in Milvus

    :param collection: collection object
    :param data: QA dataset
    :param model: model object
    :return: ([ids], [question_data], [answer_data])
    """
    try:

        # collection = Collection(name=collection.name, schema=collection.schema)
        collection.load()
        num_entities = collection.num_entities
        log.info(f"Is collection empty: {collection.is_empty}")
        log.info(f"Number of entities in collection: {num_entities}")
        # Get questions and answers.
        question_data = np.array(data['question'].tolist(), dtype=object)
        answer_data = np.array(data['answer'].tolist(), dtype=object)
        dataset_size = len(question_data)
        log.debug(f"\nDataset entity count: {dataset_size}")
        # Check if collection is empty
        if num_entities < dataset_size:
            if not model:
                raise ValueError("Model object is of None Type.")
            else:
                log.info("Model already loaded!")

            # Generate embeddings
            log.info("Generating raw embeddings... Loading......")
            answer_embeddings = encode_data(question_data, model)
            # log.info("Generating normalized embeddings... Loading......")
            # sentence_embeddings = normalize(sentence_embeddings).tolist()
            log.info("Embeddings generated successfully!")
            # Load the collection and Store embeddings in Milvus
            collection.load()
            # Insert embeddings into the collection
            mr = collection.insert([answer_embeddings])
            log.info(f"Insertion count: {mr.insert_count}")
            num_entities = collection.num_entities
            log.info(f"Number of entities in collection: {num_entities}")
            ids = mr.primary_keys
            if len(ids) != len(answer_embeddings):
                raise Exception("Number of ids and embeddings do not match!"
                                f"Number of ids: {len(ids)} \nNumber of embeddings: {len(answer_embeddings)}"
                                f"Something went wrong while inserting embeddings into the collection!")
            log.info("Embeddings generated and stored successfully!"
                     f"Number of entities in collection: {collection.num_entities}")
            return ids, question_data, answer_data
        else:
            log.info("\nEmbeddings already generated and stored!"
                     f"\nNumber of entities in collection: {collection.num_entities}"
                     f"\nCollection data: \n{collection.indexes.pop().to_dict()} ")
            # Get the ids of the entities in the collection
            ids = DataFrame(collection.query("id > 0", output_fields=["id"], limit=dataset_size)).values.tolist()
            ids = [id[0] for id in ids]
            # log.debug(f"IDs: \n{ids}")
            # Throw exception if the number of ids is less than the number of entities in the dataset
            if len(ids) < dataset_size:
                log.error(f"Number of ids: {len(ids)}")
                # log.error(f"IDs: \n{ids}")
                raise Exception("Number of ids in collection is less than the number of entities in the dataset!")

            log.info(f"Number of ids: {len(ids)}")
            # log.info(f"IDs: \n{ids}")
            return ids, question_data, answer_data
    except Exception as e:
        log.error(f'Error while generating and storing embeddings: \nModel: {model} \nCollection: {collection} \n{e}')
        log.error(traceback.format_exc())
        raise e


# Inserting IDs and Questions-answer Combos into PostgreSQL
def load_data_to_mysql(cursor: pymysql.Connection.cursor, conn: pymysql.Connection, table_name, data) -> None:
    """
    Loads data into MySQL
    Inserts the ids, questions and answers into the table

    :param cursor: cursor object
    :param conn: connection object
    :param table_name: name of the table
    :param data: data to be loaded
    :return: None
    """
    insert_statement = f"INSERT INTO {table_name} (id, question, answer) VALUES (%s, %s, %s) ;"
    log.debug(f"Insert statement: {insert_statement}")
    # check to see if the table exists
    check_table = f"SHOW TABLES LIKE {table_name};"
    # check if the data to be inserted is already present
    # check_sql = f"SELECT COUNT(*) FROM {table_name} WHERE id = %s;"
    check_count = f"SELECT COUNT(id) FROM {MYSQL_DATABASE}.{table_name} LIMIT 1;"
    create_table_sql = f"CREATE TABLE {MYSQL_DATABASE}.{table_name} " \
                       f"(idx MEDIUMINT NOT NULL AUTO_INCREMENT, " \
                       f"id VARCHAR(128) NOT NULL, " \
                       f"question TEXT NOT NULL, answer TEXT NOT NULL, PRIMARY KEY (idX))" \
                       f" ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
    try:
        cursor.execute(f"USE {MYSQL_DATABASE};")
        log.debug(f"Using database: {MYSQL_DATABASE}")
        results = cursor.execute(check_count)
        log.debug(f"Database exists: {results}")
        exit(0)
        # if cursor.execute(check_table) == 0:
        #
        #     log.info(f"Table {table_name} does not exist!")
        #     log.info(f"Creating table {table_name}...")
        #
        #     cursor.execute(create_table_sql)
        #     conn.commit()
        #     log.info(f"Table {table_name} created successfully!")
        #
        # cnt = 0
        # while True:
        #     try:
        #         rows: List = batch_retrival(data, 1000).__next__().tolist()
        #         result = cursor.execute(check_count)
        #         log.debug(f"Number of records in table: {result}")
        #         log.debug(f"Number of records in data: \n{rows}")
        #         # result = cursor.fetchone()[0]
        #         if result < len(data) + 1:
        #             # for row in rows:
        #             #     cursor.execute(insert_statement, row)
        #             cursor.executemany(query=insert_statement, args=rows)
        #             # log.debug(f"Number of records inserted: {var}")
        #             conn.commit()
        #             cnt += 1
        #             if cnt == 0:
        #                 log.info("MYSQL loads data to table: {} successfully".format(table_name))
        #             result = cursor.execute(check_count)
        #         else:
        #             log.info("MYSQL loads data to table: {} successfully".format(table_name))
        #             break
        #     except StopIteration:
        #         break
        # log.info("MYSQL loads data to table: {} successfully. Number of Records: {}".format(table_name, cnt))
    except Exception as e:
        log.error(f'\nError while loading data to MySQL: \n{str(e.args[1]).__contains__("")} ')
        log.error(traceback.format_exc())


# Combine the id of the vector and the question data into a list
def format_data(ids, question_data, answer_data) -> List:
    """
    Formats data to be loaded into MySQL

    :param ids: ids of the vectors
    :param question_data: questions
    :param answer_data: answers
    :return: formatted data
    """
    try:
        data = []
        for i in range(len(ids)):
            value = (f"{ids[i]}", f"{question_data[i]}", f"{answer_data[i]}")
            # log.debug(f"Value: \n{value}")
            data.append(value)
        # data = np.array(data, dtype=object)
        log.info("Data formatted successfully")
        log.debug(f"Formatted data count: {len(data)}")
        return data
    except Exception as e:
        log.error(f'Error while formatting data: {e}')
        log.error(traceback.format_exc())
        raise e


# Search
# Processing Query
def generate_query_embeddings(question, model) -> List:
    """
    Generates embeddings for the query

    :param question: query
    :param model: BERT model
    :return: query embeddings
    """
    try:
        embed = model.encode(question)
        embed = embed.reshape(1, -1)
        embed = normalize(embed)
        query_embeddings = embed.tolist()
        log.info("Query embeddings generated successfully")
        return query_embeddings
    except Exception as e:
        log.error(f'Error while generating query embeddings: \nQuestion: {question} \nModel: {model} \n{e}')
        log.error(traceback.format_exc())
        raise e


def search_in_milvus(collection: Collection, query_embeddings) -> SearchResult:
    """
    Searches for the query in Milvus

    :param collection: collection object
    :param query_embeddings: query embeddings
    :return: results list
    """
    try:
        search_params = {"metric_type": 'IP', "params": {"nprobe": 16}}
        log.info("Partitions: {}".format(collection.partitions))
        # Load collection
        collection.load()
        # Search
        results = collection.search(query_embeddings, anns_field="embedding", param=search_params, limit=5)
        log.info("Milvus searches data successfully")
        log.info("Search results: {}".format(len(results)))
        return results
    except Exception as e:
        log.error(f'Error while searching in Milvus: \nCollection: {collection} \n{e}')
        log.error(traceback.format_exc())
        raise e


# Getting the Similar Questions
def get_similar_questions(cursor, ids, table_name) -> List:
    """
    Gets the similar questions from MySQL

    :param cursor: cursor object
    :param ids: ids of the similar questions
    :param table_name: name of the table
    :return: list of similar questions
    """
    str_ids = str(ids).replace('[', '').replace(']', '')
    sql = "select question from " + table_name + " where id in (" + str_ids + ") order by field (id," + str_ids + ");"
    try:
        if ids is None or len(ids) == 0:
            return []
        cursor.execute(sql)
        results = cursor.fetchall()
        results = [res[0] for res in results]
        return results
    except Exception as e:
        log.error(f'Error while getting similar questions: \nSql: \n{sql} \n{e} ')
        log.error(traceback.format_exc())
        raise e


# Get the answer
def search_by_similar_questions(cursor, table_name, question=None) -> List:
    """
    Searches for the answer by similar questions

    :param cursor: cursor object
    :param question: question
    :param table_name: name of the table
    :return: answer list
    """
    sql = "select answer from " + table_name + f" where question = `{question}`;"
    try:
        if question is None or len(question) == 0:
            raise Exception("Question is None or empty")
        sql = "select answer from " + table_name + " where question in ('" + question[0] + "');"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows is None or len(rows) == 0:
            raise Exception("No answer found")
        return rows
    except Exception as e:
        log.error(f'Error while searching by similar questions: \nSql: \n{sql} \n{e} ')
        log.error(traceback.format_exc())
        return []


# Extract answer
def get_answer(rows) -> str:
    """
    Extracts the answer from the rows

    :param rows: rows of the table
    :return: answer string
    """
    try:
        if rows is None or len(rows) == 0:
            return "Sorry, No answer found."
        return rows[0][0]
    except Exception as e:
        log.error(f'Error while getting answer: \nRows: {rows} \n{e}')
        log.error(traceback.format_exc())
        raise e


# API
def get_response_by_question(question, table_name=MILVUS_COLLECTION) -> Any:
    try:
        # Setting up milvus and mysql connection
        conn, cursor, collection = connect_to_milvus_and_mysql()
        # Creating Collection and Setting Index
        collection = create_collection(table_name=table_name)
        # Creating Table in MySQL
        create_table_in_mysql(cursor=cursor, table_name=table_name)
        # Processing and Storing QA Dataset
        ids, question_data, answer_data = generate_and_store_embeddings(collection=collection)
        # Format the data
        data = format_data(ids=ids,
                           question_data=question_data,
                           answer_data=answer_data)
        # Inserting IDs and Questions-answer Combos into PostgreSQL

        load_data_to_mysql(cursor, conn, table_name, data)

        answer = process_query(cursor, question, collection)
        return answer
    except Exception as e:
        log.error(f'Error while getting response by question: \nQuestion: {question} \n{e}')
        log.error(traceback.format_exc())
        raise e


def process_query(cursor, question: str, collection: Collection, table_name=MILVUS_COLLECTION,
                  model=MODEL_SELECTION['sentence_transformers']) -> str:
    """
    Processes the query

    :param cursor: cursor object
    :param question: question
    :param table_name: name of the table
    :param model: model name
    :param collection: collection object
    """
    try:
        log.info("Processing query: {}".format(question))
        # Processing Query
        query_embeddings = generate_query_embeddings(question, model)
        log.info("Query embeddings generated successfully")
        # Search
        results = search_in_milvus(collection=collection, query_embeddings=query_embeddings)
        log.info("Search results: {}".format(len(results)))
        # Getting the Similar Questions
        ids = [str(x.id) for x in results[0]]
        similar_questions = get_similar_questions(cursor, ids, table_name)
        log.info("Similar questions: {}".format(similar_questions))
        # Get the answer
        rows = search_by_similar_questions(cursor, table_name, similar_questions, )
        # Extract answer
        answer = get_answer(rows)
        return answer
    except Exception as e:
        log.error(f'Error while processing query: \nQuestion: {question} \n{e}')
        log.error(traceback.format_exc())


def chatbot_handler(question) -> str:
    conn, cursor, collection = connect_to_milvus_and_mysql()
    return process_query(cursor, question, collection)


def diff_texts(text1: str, text2: str):
    d = Differ()
    return [
        (token[2:], token[0] if token[0] != " " else None)
        for token in d.compare(text1, text2)
    ]


# def diff_texts(text1: str, text2: str):
#     d = Differ()
#     diff = d.compare(text1, text2)
#     output = []
#
#     for token in diff:
#         action = token[0]
#         word = token[2:]
#         if action == " ":
#             output.append((word, None))
#         else:
#             output.append((word, action))
#     return output


def handle_diff(text: str):
    result_text = chatbot_handler(text)
    return diff_texts(text, result_text)


def response_handler(message, state: List = None):
    bot_message = chatbot_handler(message)
    # bot_message = diff_texts(message, bot_message)
    state.append((message, bot_message))
    time.sleep(1)
    return "", state

# def transcribe(__input__, state=None):
#     chat_history = []
#     if state is None:
#         state = ""
#     if isinstance(__input__, str):
#         state += str(response_handler(__input__, state))
#     elif isinstance(__input__, (bytes, bytearray, gradio.Audio)):
#         text = p(__input__)["text"]
#         state += str(response_handler(text, state))
#     log.info("\nState: \n{}".format(state))
#     return state, state


# def transcribe(audio, state=""):
#     time.sleep(2)
#     text = p(audio)["text"]
#     state += text + " "
#     log.info("\nState: \n{}".format(state))
#     return state, response_handler(state, [])
