# Connecting to Servers
#
# We first start off by connecting to the servers. In this case the docker containers are running
# on localhost and the ports are the default ports.

# Connecting to Milvus, BERT and Postgresql
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import pymysql
import os

# Connecting to Milvus, BERT and Postgresql
connections.connect(alias='default',
                    user='milvus',
                    password='developer',
                    host='127.0.0.1',
                    port='19530')
# Create a vector collection in MySQL
conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='milvus',
                       password='developer',
                       database='milvus_meta',
                       local_infile=True)
# Create a vector collection in MySQL
cursor = conn.cursor()

# Creating Collection and Setting Index
#
# 1. Creating the Collection
#
# A collection in Milvus is similar to a table in a relational database, and is used for storing all the vectors.
# The required parameters for creating a collection are as follows:
#
# collection_name: the name of a collection.
# dimension: BERT generates 728-dimensional vectors.
# index_file_size: how large each data segment will be within the collection.
# metric_type: the distance formula being used to calculate similarity. In this example we are using Inner product (IP).

TABLE_NAME = 'question_answering'

# Deleting previouslny stored table for clean run
if utility.has_collection(TABLE_NAME):
    collection = Collection(name=TABLE_NAME)
    collection.drop()

field1 = FieldSchema(name="id", dtype=DataType.INT64, descrition="int64", is_primary=True, auto_id=True)
field2 = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, descrition="float vector", dim=768,
                     is_primary=False)
schema = CollectionSchema(fields=[field1, field2], description="collection description")
collection = Collection(name=TABLE_NAME, schema=schema)

# 2. Setting an Index
#
# After creating the collection we want to assign it an index type. This can be done before or
# after inserting the data. When done before, indexes will be made as data comes in and fills the
# data segments. In this example we are using IVF_FLAT which requires the 'nlist' parameter.
# Each index types carries its own parameters. More info about this param can be found here.

default_index = {"index_type": "IVF_FLAT", "metric_type": 'IP', "params": {"nlist": 200}}
collection.create_index(field_name="embedding", index_params=default_index)

# Creating Table in MySQL
#
# MySQL will be used to store the Milvus ID and its corresponding question-answer combo.

# Deleting previouslny stored table for clean run
drop_table = "DROP TABLE IF EXISTS " + TABLE_NAME + ";"
cursor.execute(drop_table)

try:
    sql = "CREATE TABLE if not exists " + TABLE_NAME + " (id TEXT, question TEXT, answer TEXT);"
    cursor.execute(sql)
    print("create MySQL table successfully!")
except Exception as e:
    print("can't create a MySQL table: ", e)

# Processing and Storing QA Dataset
#
# 1. Generating Embeddings
#
# In this example we are using the sentence_transformer library to encode the sentence into
# vectors. This library uses a modified BERT model to generate the embeddings, and in this
# example we are using a model pretrained using Microsoft's mpnet. More info can be found here.

from sentence_transformers import SentenceTransformer
import pandas as pd
from sklearn.preprocessing import normalize

DATASET_DATA = f'{os.getcwd()}/Resources/datasets/questions_answers.csv'
model = SentenceTransformer('all-mpnet-base-v2')

# Get questions and answers.
data = pd.read_csv(DATASET_DATA)
question_data = data['question'].tolist()
answer_data = data['answer'].tolist()

sentence_embeddings = model.encode(question_data)
sentence_embeddings = normalize(sentence_embeddings).tolist()

# 2. Inserting Vectors into Milvus
#
# Since this example dataset contains only 100 vectors, we are inserting all of them as one batch insert.

mr = collection.insert([sentence_embeddings])
ids = mr.primary_keys
print(len(ids))

# status, ids = milv.insert(collection_name=TABLE_NAME, records=sentence_embeddings)
# print(status)

# 3. Inserting IDs and Questions-answer Combos into PostgreSQL
#
# In order to transfer the data into Postgres, we are creating a new file that combines all the
# data into a readable format. Once created, we pass this file into the Postgress server through
# STDIN due to the Postgres container not having access to the file locally.

import os


# Combine the id of the vector and the question data into a list
def format_data(ids, question_data, answer_data):
    data = []
    for i in range(len(ids)):
        value = (str(ids[i]), question_data[i], answer_data[i])
        data.append(value)
    return data


def load_data_to_mysql(cursor, conn, table_name, data):
    sql = "insert into " + table_name + " (id,question,answer) values (%s,%s,%s);"
    try:
        cursor.executemany(sql, data)
        conn.commit()
        print("MYSQL loads data to table: {} successfully".format(table_name))
    except Exception as e:
        print("MYSQL ERROR: {} with sql: {}".format(e, sql))


load_data_to_mysql(cursor, conn, TABLE_NAME, format_data(ids, question_data, answer_data))

# Search
#
# 1. Processing Query
#
# When searching for a question, we first put the question through the same model to generate an
# embedding. Then with that embedding vector we can search for similar embeddings in Milvus.

SEARCH_PARAM = {'nprobe': 40}

query_vec = []

question = "What is AAA?"

embed = model.encode(question)
embed = embed.reshape(1, -1)
embed = normalize(embed)
query_embeddings = embed.tolist()

collection.load()

search_params = {"metric_type": 'IP', "params": {"nprobe": 16}}

results = collection.search(query_embeddings, anns_field="embedding", param=search_params, limit=5)

# status, results = milv.search(collection_name=TABLE_NAME, query_records=query_embeddings, top_k=5,
# params=SEARCH_PARAM)

# 2. Getting the Similar Questions
#
# There may not have questions that are similar to the given one. So we can set a threshold value, here we use 0.5,
# and when the most similar distance retrieved is less than this value, a hint that the system doesn't include the
# relevant question is returned. We then use the result ID's to pull out the similar questions from the Postgres
# server and print them with their corresponding similarity score.

ids = [str(x.id) for x in results[0]]


def search_by_milvus_ids(cursor, ids, table_name):
    str_ids = str(ids).replace('[', '').replace(']', '')
    sql = "select question from " + table_name + " where id in (" + str_ids + ") order by field (id," + str_ids + ");"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        results = [res[0] for res in results]
        return results
    except Exception as e:
        print("MYSQL ERROR: {} with sql: {}".format(e, sql))


similar_questions = search_by_milvus_ids(cursor, ids, TABLE_NAME)

distances = [x.distance for x in results[0]]

res = dict(zip(similar_questions, distances))

print('There are similar questions in the database, here are the closest matches:\n{}'.format(res))

# 3. Get the answer
#
# After getting a list of similar questions, choose the one that you feel is closest to yours. Then you can use that
# question to find the corresponding answer in Postgres.

sql = "select answer from " + TABLE_NAME + " where question = '" + similar_questions[0] + "';"

cursor.execute(sql)
rows = cursor.fetchall()
print("Question:")
print(question)
print("Answer:")
print(rows[0][0])
