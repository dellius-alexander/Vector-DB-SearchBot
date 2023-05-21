import traceback
from pymilvus import Collection, FieldSchema, DataType
import gradio as gr
from database.mysql import MySQLDatabase
from milvus.milvus_helper import MilvusClient
from milvus.question_answering import load_data_to_mysql, generate_and_store_embeddings, format_data, handle_diff
from myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)

TABLE_NAME = 'question_answering'


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
    # # Gradio Interface
    demo = gr.Interface(
        fn=handle_diff,
        inputs=[
            gr.Textbox(label="Query Search",
                       info="Ask me Question and Press Submit",
                       lines=3),],
        outputs=[
            gr.HighlightedText(
                label="Diff",
                combine_adjacent=True,
                show_legend=True,
            )
            .style(color_map={"+": "red", "-": "green"}),
        ],
        theme=gr.themes.Base(),
        description="This is a simple question and answering system that uses a corpus of 1000 questions and answers.",
        info=gr.Markdown(about),
    )

    demo.launch(share=False, inline=True, inbrowser=True, debug=True)


if __name__ == '__main__':
    try:

        TABLE_NAME = 'question_answering'
        mysql_db = MySQLDatabase(host='127.0.0.1',
                                 port=3306,
                                 user='milvus',
                                 password='developer',
                                 database='milvus_meta')
        if not mysql_db:
            raise Exception("Failed to connect to MySQL Server: {}".format(mysql_db))
        milvus_client = MilvusClient(**{
            "alias": 'default',
            "host": '127.0.0.1',
            "port": '19530',
            "user": 'milvus',
            "password": 'developer'})
        if not milvus_client:
            raise Exception("Failed to connect to Milvus Server: {}".format(milvus_client))
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, descrition="int64", is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, descrition="float vector", dim=768,
                        is_primary=False)
        ]
        collection = milvus_client.create_collection(TABLE_NAME, fields)
        if collection is None:
            raise Exception("Failed to create collection: {}".format(TABLE_NAME))
        log.info("collection: {}".format(collection))
        ids, question_data, answer_data = generate_and_store_embeddings(collection=collection)
        load_data_to_mysql(mysql_db.cursor, mysql_db.connection,
                           TABLE_NAME, format_data(ids, question_data, answer_data))

        chatbot(collection=collection)
    except Exception as e:
        log.error("Error: {}".format(e))
        log.error(traceback.format_exc())