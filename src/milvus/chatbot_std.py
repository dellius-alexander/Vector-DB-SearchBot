import traceback
from pymilvus import Collection, FieldSchema, DataType
import gradio as gr
from question_answering import response_handler, generate_and_store_embeddings, format_data, load_data_to_mysql
from myLogger.Logger import getLogger as GetLogger
from milvus_helper import MilvusClient
from database.mysql import MySQLDatabase

log = GetLogger(__name__)


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
                   api_name="query_msg", )  # query chatbot
        query_btn.click(fn=response_handler,
                        inputs=[msg, __chatbot],
                        outputs=[msg, __chatbot],
                        api_name="query_btn")  # query chatbot
        clear.click(lambda: None, None, __chatbot, queue=False)  # clear chatbot
    demo.launch(inline=False,
                debug=True,
                share=False,
                show_tips=True,
                show_api=True,
                ) # launch the chatbot


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
