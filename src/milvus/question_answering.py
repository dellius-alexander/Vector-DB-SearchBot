import time
import traceback
from typing import List, Any, Dict
import pymysql
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility, SearchResult
from sentence_transformers import SentenceTransformer
import pandas as pd
from difflib import Differ
from sklearn.preprocessing import normalize
from myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)

# Connecting to Milvus, BERT and Postgresql
USERNAME = "milvus"
PASSWORD = "developer"
HOST = "127.0.0.1"
MILVUS_PORT = 19530
MYSQL_PORT = 3306
DATASET_DATA = '../Resources/datasets/questions_answers.csv'
DATABASE_NAME = 'milvus_meta'
TABLE_NAME = 'question_answering'
CONNECTION_ALIAS = 'default'
# Model Selection for Sentence Transformation
MODEL = SentenceTransformer('all-mpnet-base-v2')


# Setting up milvus and mysql connection
def connect_to_milvus_and_mysql():
    """
    Connects to Milvus and MySQL
    """
    try:
        connections.connect(alias=CONNECTION_ALIAS, user=USERNAME, password=PASSWORD, host=HOST, port=MILVUS_PORT)

        conn = pymysql.connect(host=HOST, port=MYSQL_PORT, user=USERNAME, password=PASSWORD, database=DATABASE_NAME,
                               local_infile=True)
        cursor = conn.cursor()
        log.debug(f'Connection with {CONNECTION_ALIAS} found {connections.has_connection(alias=CONNECTION_ALIAS)}')
        return conn, cursor, Collection(name=TABLE_NAME)
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


def generate_embeddings(data: Dict):
    """
    Generates embeddings for the questions and answers

    :param data: data object
    :return: sentence_embeddings
    """
    global MODEL
    try:
        if MODEL is None:
            MODEL = SentenceTransformer('all-mpnet-base-v2')
        # Get questions and answers.
        question_data = data['question'].tolist()
        answer_data = data['answer'].tolist()
        # Generate embeddings
        sentence_embeddings = MODEL.encode([question_data, answer_data])
        log.info(f"Raw embeddings: \n{sentence_embeddings}")
        sentence_embeddings = normalize(sentence_embeddings).tolist()
        log.info(f"Normalized embeddings: \n{sentence_embeddings}")
        return sentence_embeddings, data
    except Exception as e:
        log.error(f'Error while generating embeddings: \nModel: {MODEL} \n{e}')
        log.error(traceback.format_exc())
        raise e


# Processing and Storing QA Dataset
def generate_and_store_embeddings(collection: Collection):
    """
    Generates embeddings for the questions and answers and stores them in Milvus

    :param model: BERT model
    :param collection: collection object
    :return: ids, question_data, answer_data
    """
    global MODEL
    try:
        data = pd.read_csv(DATASET_DATA)
        collection = Collection(name=collection.name, schema=collection.schema)
        collection.load()
        log.info(f"Is collection empty: {collection.is_empty}")
        log.info(f"Number of entities in collection: {collection.num_entities}")

        if collection.num_entities != data.__len__():
            if MODEL is None:
                MODEL = SentenceTransformer('all-mpnet-base-v2')
                log.info("Model loaded successfully!")
            else:
                log.info("Model already loaded!")
            # Get questions and answers.
            question_data = data['question'].tolist()
            answer_data = data['answer'].tolist()
            # Generate embeddings
            log.info("Generating raw embeddings...loading......")
            sentence_embeddings = MODEL.encode(answer_data)
            log.info("Generating normalized embeddings...loading......")
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
        log.error(f'Error while generating and storing embeddings: \nModel: {MODEL} \nCollection: {collection} \n{e}')
        log.error(traceback.format_exc())
        raise e


# Inserting IDs and Questions-answer Combos into PostgreSQL
def load_data_to_mysql(cursor, conn, table_name, data) -> None:
    """
    Loads data into MySQL

    :param cursor: cursor object
    :param conn: connection object
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
            cursor.execute(check_sql, (row[0],))
            result = cursor.fetchone()[0]
            if result == 0:
                cursor.execute(sql, row)
                conn.commit()
                cnt += 1
                if cnt == 0:
                    log.info("MYSQL loads data to table: {} successfully".format(table_name))
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
    sql = "select answer from " + table_name + " where question = `None`;"
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
def get_response_by_question(question) -> Any:
    try:
        # Setting up milvus and mysql connection
        conn, cursor, collection = connect_to_milvus_and_mysql()
        # Creating Collection and Setting Index
        collection = create_collection(table_name=TABLE_NAME)
        # Creating Table in MySQL
        create_table_in_mysql(cursor=cursor, table_name=TABLE_NAME)
        # Processing and Storing QA Dataset
        ids, question_data, answer_data = generate_and_store_embeddings(collection=collection)
        # Inserting IDs and Questions-answer Combos into PostgreSQL
        if len(ids) > 0:
            load_data_to_mysql(cursor, conn, TABLE_NAME, format_data(ids=ids,
                                                                     question_data=question_data,
                                                                     answer_data=answer_data))

        answer = process_query(cursor, question, collection)
        return answer
    except Exception as e:
        log.error(f'Error while getting response by question: \nQuestion: {question} \nMODEL: {MODEL} \n{e}')
        log.error(traceback.format_exc())
        raise e


def process_query(cursor, question: str, collection: Collection) -> str:
    """
    Processes the query

    :param cursor: cursor object
    :param question: question
    :param collection: collection object
    """
    log.info("Processing query: {}".format(question))
    # Processing Query
    query_embeddings = generate_query_embeddings(question, MODEL)
    log.info("Query embeddings generated successfully")
    # Search
    results = search_in_milvus(collection=collection, query_embeddings=query_embeddings)
    log.info("Search results: {}".format(len(results)))
    # Getting the Similar Questions
    ids = [str(x.id) for x in results[0]]
    similar_questions = get_similar_questions(cursor, ids, TABLE_NAME)
    log.info("Similar questions: {}".format(similar_questions))
    # Get the answer
    rows = search_by_similar_questions(cursor, TABLE_NAME, similar_questions, )
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


def handle_diff(text: str):
    result_text = chatbot_handler(text)
    return diff_texts(text, result_text)


def response_handler(message, chat_history=None):
    if chat_history is None:
        chat_history = []
    bot_message = chatbot_handler(message)
    # bot_message = diff_texts(message, bot_message)
    chat_history.append((message, bot_message))
    time.sleep(1)
    return "", chat_history
