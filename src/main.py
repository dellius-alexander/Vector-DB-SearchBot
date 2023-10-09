import logging
import traceback

import numpy as np
import pandas as pd
from pymilvus import Collection, FieldSchema, DataType
import gradio as gr
from src.milvus.question_answering import response_handler, generate_and_store_embeddings, \
    format_data, load_data_to_mysql, encode_data
from src.myLogger.Logger import getLogger as GetLogger
from src.milvus.milvus_helper import MilvusClient
from src.database.mysql import MySQLDatabase
from src.config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, \
    MILVUS_HOST, MILVUS_PORT, MILVUS_USER, MILVUS_PASSWORD, MILVUS_COLLECTION, \
    MYSQL_DATABASE_TABLE_NAME, APP_HOST, APP_PORT, MILVUS_CONNECTION_ALIAS, DATASET_PATH, MODEL_SELECTION

log = GetLogger(name=__name__, level=logging.DEBUG)


def chatbot(collection: Collection, **kwargs):
    """
    Chatbot interface for the QA system using gradio

    :param collection: collection object
    :return: None
    """
    log.info("kwargs: {}".format(kwargs))
    about = """This is a simple question and answering system that uses a corpus of 1000 questions and answers.
    <br> The system uses a pre-trained model to generate embeddings for the questions and answers.
    <br> The embeddings are stored in Milvus and the questions and answers are stored in MySQL. When a <br>
    query is submitted, the system generates embeddings for the query and searches for similar embeddings <br>
    in Milvus vector database. The system then retrieves the similar questions and answers from MySQL <br>
    that matches the indexes of the retried vectors and returns the answer corresponding to the nearest <br>
    candidate or best search result found. <br> <br>

    The system is built using Milvus, MySQL, Gradio, and HuggingFace Sentence Transformers all-mpnet-base-v2 
    model.<br> <br>

    References: <br><br> <ul> <li><a href="https://github.com/milvus-io/bootcamp/blob/v2.0.2/solutions
    /question_answering_system/question_answering.ipynb">Milvus Bootcamp</a></li> <li><a 
    href="https://milvus.io/docs/question_answering_system.md">Milvus Documentation Question and Answering</a></li> 
    </ul>"""
    collection.load()

    with gr.Blocks() as demo:
        gr.Markdown("Simple Question and Answering System featuring corpus of 1000 questions and answers.")
        __chatbot = gr.Chatbot(label="QA Chatbot")
        msg = gr.Textbox(label="Ask me Question and Press Enter")
        query_btn = gr.Button("Submit Query")
        clear = gr.Button("Clear")
        with gr.Accordion(label="About",
                          open=False,
                          visible=True,
                          elem_id="accordion", ):
            gr.Markdown(about)

        msg.submit(fn=response_handler,
                   inputs=[msg, __chatbot],
                   outputs=[msg, __chatbot],
                   api_name="query", )  # query chatbot
        query_btn.click(fn=response_handler,
                        inputs=[msg, __chatbot],
                        outputs=[msg, __chatbot])  # query chatbot
        clear.click(lambda: None, None, __chatbot, queue=False)  # clear chatbot
        demo.launch(inline=False,
                    debug=True,
                    share=False,
                    show_tips=True,
                    show_api=True,
                    server_name=APP_HOST,
                    server_port=int(APP_PORT),
                    )  # launch the chatbot


def main():
    try:

        mysql_db = MySQLDatabase(host=MYSQL_HOST,
                                 port=int(MYSQL_PORT),
                                 user=MYSQL_USER,
                                 password=MYSQL_PASSWORD,
                                 database=MYSQL_DATABASE)
        if not mysql_db:
            raise Exception("Failed to connect to MySQL Server: {}".format(mysql_db))
        log.debug(f"MySQL Database: \n{mysql_db}")

        milvus_client = MilvusClient(**{
            "alias": MILVUS_CONNECTION_ALIAS,
            "host": MILVUS_HOST,
            "port": int(MILVUS_PORT),
            "user": MILVUS_USER,
            "password": MILVUS_PASSWORD})

        if not milvus_client:
            raise Exception("Failed to connect to Milvus Server: {}".format(milvus_client))

        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, descrition="int64", is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, descrition="float vector", dim=768,
                        is_primary=False)
        ]
        __collection = milvus_client.create_collection(MYSQL_DATABASE_TABLE_NAME, fields)
        if __collection is None:
            raise Exception("Failed to create collection: {}".format(MYSQL_DATABASE_TABLE_NAME))
        log.info("collection: \n{}".format(__collection))

        ids, question_data1, answer_data1 = generate_and_store_embeddings(collection=__collection,
                                                                        data=data,
                                                                        model=model)
        formatted_data = format_data(ids, question_data, answer_data)
        load_data_to_mysql(mysql_db.cursor,
                           mysql_db.connection,
                           MYSQL_DATABASE_TABLE_NAME,
                           formatted_data)
        # chatbot(collection=__collection)
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


if __name__ == '__main__':
    try:
        model = MODEL_SELECTION['sentence_transformers']
        data = pd.read_csv(DATASET_PATH)
        answer_data = data['answer'].values
        question_data = data['question'].values
        # random_dataset = np.random.choice(data['question'].values, 99)
        # embeddings = encode_data(data=random_dataset, model=model)
        # log.info(f"Embeddings shape: {embeddings.shape}")
        main()

    except Exception as e:
        log.error("Error: {}".format(e))
        log.error(traceback.format_exc())
