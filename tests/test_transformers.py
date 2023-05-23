import csv
import json
import os
import traceback

import pandas as pd
import torch
import transformers
from pymilvus import connections, FieldSchema, DataType, CollectionSchema, Collection
from pymilvus.orm import utility
from transformers import AutoModelWithLMHead, AutoTokenizer, AutoModel, QuestionAnsweringPipeline

from src.myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)

MODEL_SELECTION = 'bert-large-uncased-whole-word-masking-finetuned-squad'

DATASET_DATA = f'{os.getcwd()}/src/Resources/datasets/questions_answers.csv'
COLLECTION_NAME = 'question_answer'

# Prepare the Data
df = pd.read_csv(DATASET_DATA)
log.info(df.head(10))
log.info(df.info())
id_answer = df.set_index('id')['answer']
id_question = df.set_index('id')['question']


def test_tokenizer():
    utility.connections.connect(alias='default',
                                host='127.0.0.1',
                                port='19530',
                                user='alpha',
                                password='developer')
    collection_name = 'test_tokenizer'
    dim = 768
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)
    # FieldSchema(name='question', dtype=DataType.VARCHAR, descrition='questions', max_length=500, is_primary=False),
    fields = [
        FieldSchema(name='id', dtype=DataType.INT64, descrition='ids', max_length=500, is_primary=True,
                    auto_id=False),
        FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, descrition='embedding vectors', dim=dim)
    ]
    schema = CollectionSchema(fields=fields, description='tokenizer search')
    collection = Collection(name=collection_name, schema=schema)

    # create IVF_FLAT index for collection.
    index_params = {
        'metric_type': 'L2',
        'index_type': "IVF_FLAT",
        'params': {"nlist": 2048}
    }
    collection.create_index(field_name="embedding", index_params=index_params)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_SELECTION)
    cnt = 0
    idx = []
    for question in id_question:
        embedding = tokenizer.encode_plus(question, return_tensors="pt")
        log.info(question)
        log.info(embedding)
        idx.append(cnt)
        # log.info(tokenizer.encode_plus(question, return_tensors="pt"))
        insert_status = collection.insert(data=[embedding])
        log.info(insert_status)
        cnt += 1
        if cnt > 5:
            break


def test_tokenizer_v2():
    try:
        # Create Milvus connection and connect to database

        status = utility.connections.connect(alias='default',
                                             host='127.0.0.1',
                                             port='19530',
                                             user='alpha',
                                             password='')
        log.info(status)
        # Create a vector collection
        collection_name = 'qa_collection'
        dim = 768
        index_file_size = 32

        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)


        fields = [
            FieldSchema(name='id', dtype=DataType.INT64, descrition='ids', max_length=500, is_primary=True,
                        auto_id=False),
            # FieldSchema(name='question_embedding', dtype=DataType.FLOAT_VECTOR, descrition='question embedding vectors', dim=dim),
            FieldSchema(name='answer_embedding', dtype=DataType.FLOAT_VECTOR, descrition='answer embedding vectors', dim=dim)
        ]
        schema = CollectionSchema(fields=fields, description='tokenizer search')
        collection = Collection(name=collection_name, schema=schema)

        # create IVF_FLAT index for collection.
        index_params = {
            'metric_type': 'L2',
            'index_type': "IVF_FLAT",
            'params': {"nlist": 2048}
        }
        # collection.create_index(field_name="question_embedding", index_params=index_params)
        collection.create_index(field_name="answer_embedding", index_params=index_params)

        # Create BERT model
        bert_model = transformers.BertModel.from_pretrained('bert-base-uncased')
        log.info(json.dumps(dir(bert_model), indent=2))

        # Read data from csv
        with open(DATASET_DATA) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                # Get the data fields
                _id = row[0]
                question = row[1]
                answer = row[2]

                # Tokenize the query and answer data using BERT
                question_tokens = bert_model.encoder.encode(question)
                answer_tokens = bert_model.encoder.encode(answer)

                # Create a tensor of query and answer tokens
                question_tokens_tensor = torch.tensor([question_tokens])
                answer_tokens_tensor = torch.tensor([answer_tokens])

                # Use BERT to create a vector representation of query and answer tokens
                question_vector = bert_model(question_tokens_tensor)[0][0]
                answer_vector = bert_model(answer_tokens_tensor)[0][0]

                # Convert vectors to float
                question_vector_float = question_vector.float()
                answer_vector_float = answer_vector.float()

                # Insert vectors into Milvus
                collection.insert([answer_vector_float])

        # Close the connection to the database
        # utility.connections.disconnect(alias='default')

        # Create a loop to search for prompts against the Milvus vector database
        while True:
            # Is  Disability  Insurance  Required  By  Law?
            prompt = input("Please enter your prompt: ")
            # Tokenize the prompt using BERT
            prompt_tokens = bert_model.encoder(prompt, add_special_tokens=True)
            # Create a tensor of prompt tokens
            prompt_tokens_tensor = torch.tensor([prompt_tokens])
            # Use BERT to create a vector representation of the prompt tokens
            prompt_vector = bert_model(prompt_tokens_tensor)[0][0]
            # Convert vector to float
            prompt_vector_float = prompt_vector.float()
            # Search for the prompt vector in the Milvus vector database
            search_param = {
                "data": [prompt_vector_float],
                "anns_field": "embedding",
                "param": {"metric_type": "L2", "offset": 1},
                "limit": 2,
                "expr": "id > 0",
                "top_k": 1
            }
            result = collection.search(search_param)
            # Print the answer embedded in the result
            print(result[0]['embedding'])
            # convert the results back to utf-8 readable text
            print(id_answer[result[0]['id'][0]])
            print(id_question[result[0]['id'][0]])
    except Exception:
        log.error(traceback.format_exc())

