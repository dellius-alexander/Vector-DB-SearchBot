import time
import traceback
from typing import List, Any, Dict, Tuple
import pymysql
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility, SearchResult
from sentence_transformers import SentenceTransformer
import pandas as pd
from difflib import Differ
from sklearn.preprocessing import normalize
from myLogger.Logger import getLogger as GetLogger
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, \
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
        yield arr[batch_index:batch_index + batch_amount]  # yield portion of array
        batch_index += (batch_amount - 1)  # add batch amount to index
    # output rest of array if the length of the array is not a multiple of batch_amount
    if batch_index < len(arr):
        yield arr[batch_index:]


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


def generate_embeddings(data: Dict, model=None) -> Tuple[List[Any], Dict]:
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
        sentence_embeddings = model.encode([question_data, answer_data])
        log.info(f"Raw embeddings: \n{sentence_embeddings}")
        sentence_embeddings = normalize(sentence_embeddings).tolist()
        log.info(f"Normalized embeddings: \n{sentence_embeddings}")
        return sentence_embeddings, data
    except Exception as e:
        log.error(f'Error while generating embeddings: \nModel: {model} \n{e}')
        log.error(traceback.format_exc())
        raise e


# Processing and Storing QA Dataset
def generate_and_store_embeddings(collection: Collection, model=MODEL_SELECTION['sentence_transformers']):
    """
    Generates embeddings for the questions and answers and stores them in Milvus

    :param model: BERT model
    :param collection: collection object
    :return: ids, question_data, answer_data
    """
    try:
        data = pd.read_csv(DATASET_PATH)
        collection = Collection(name=collection.name, schema=collection.schema)
        collection.load()
        log.info(f"Is collection empty: {collection.is_empty}")
        log.info(f"Number of entities in collection: {collection.num_entities}")

        if collection.is_empty:
            if not model:
                raise ValueError("Model object is of None Type.")
            else:
                log.info("Model already loaded!")
            # Get questions and answers.
            question_data = data['question'].tolist()
            answer_data = data['answer'].tolist()
            # Generate embeddings
            log.info("Generating raw embeddings... Loading......")
            sentence_embeddings = model.encode(answer_data)
            log.info("Generating normalized embeddings... Loading......")
            sentence_embeddings = normalize(sentence_embeddings).tolist()
            log.info("Embeddings generated successfully!")
            collection.load()
            log.info(f"Number of entities in collection: {collection.num_entities}")
            log.info(f"Number of embeddings: {len(sentence_embeddings)}")
            # raise Exception("Number of entities in collection and embeddings do not match!")
            mr = collection.insert([sentence_embeddings])
            ids = mr.primary_keys
            log.info("Embeddings generated and stored successfully!")
            return ids, question_data, answer_data
        else:
            log.info("Embeddings already generated and stored!")
            log.info(f"Number of entities in collection: {collection.num_entities}")
            log.info(f"Collection Indexes: {collection.indexes}")
            return [], [], []
    except Exception as e:
        log.error(f'Error while generating and storing embeddings: \nModel: {model} \nCollection: {collection} \n{e}')
        log.error(traceback.format_exc())
        raise e


# Inserting IDs and Questions-answer Combos into PostgreSQL
async def load_data_to_mysql(cursor, conn, table_name, data) -> None:
    """
    Loads data into MySQL
    Inserts the ids, questions and answers into the table

    :param cursor: cursor object
    :param conn: connection object
    :param table_name: name of the table
    :param data: data to be loaded
    :return: None
    """
    sql = "insert into " + table_name + " (id, question, answer) values (%s, %s, %s);"
    # check to see if the table exists
    check_table = f"SHOW TABLES LIKE '{table_name}';"
    # check if the data to be inserted is already present
    # check_sql = f"SELECT COUNT(*) FROM {table_name} WHERE id = %s;"
    check_count = f"SELECT COUNT(id) FROM {table_name};"
    try:
        cursor.execute(f"USE {MYSQL_DATABASE};")
        if cursor.execute(check_table) == 0:
            log.info(f"Table {table_name} does not exist!")
            log.info(f"Creating table {table_name}...")
            create_table_sql = f"CREATE TABLE {table_name} (id VARCHAR(128) NOT NULL, question TEXT NOT NULL, " \
                               f"answer TEXT NOT NULL, PRIMARY KEY (id));"
            cursor.execute(create_table_sql)
            conn.commit()
            log.info(f"Table {table_name} created successfully!")
        cnt = 0
        while True:
            try:
                row: List = batch_retrival(data, 1000)
                result = cursor.execute(check_count)
                # result = cursor.fetchone()[0]
                if result < len(data) + 1 and len(row) > 0:
                    cursor.executemany(sql, row)
                    await conn.commit()
                    cnt += 1
                    if cnt == 0:
                        log.info("MYSQL loads data to table: {} successfully".format(table_name))
            except StopIteration:
                break
        log.info("MYSQL loads data to table: {} successfully. Number of Records: {}".format(table_name, cnt))
    except Exception as e:
        log.error(f'Error while loading data to MySQL. Sql insert error: \n{sql}\n{e} ')
        log.error(traceback.format_exc())
        raise e


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
            value = (str(ids[i]), question_data[i], answer_data[i])
            data.append(value)
        log.info("Data formatted successfully")
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
        # Inserting IDs and Questions-answer Combos into PostgreSQL
        load_data_to_mysql(cursor, conn, table_name, format_data(ids=ids,
                                                                 question_data=question_data,
                                                                 answer_data=answer_data))

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
