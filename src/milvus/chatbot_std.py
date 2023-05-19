
from pymilvus import Collection
import gradio as gr
from milvus.question_answering import generate_and_store_embeddings, format_data, load_data_to_mysql, \
    connect_to_milvus_and_mysql, create_collection, create_table_in_mysql, response_handler
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

        msg.submit(fn=response_handler, inputs=[msg, __chatbot], outputs=[msg, __chatbot], api_name="query_msg")
        query_btn.click(fn=response_handler, inputs=[msg, __chatbot], outputs=[msg, __chatbot], api_name="query_btn")
        clear.click(lambda: None, None, __chatbot, queue=False)  # Gradio Interface
    demo.launch(inline=False,
                debug=True,
                share=False,
                show_tips=True,
                show_api=True,
                )


if __name__ == '__main__':
    __conn__, __cursor__, __collection__ = connect_to_milvus_and_mysql()
    __collection__ = create_collection(TABLE_NAME)
    create_table_in_mysql(__cursor__, TABLE_NAME)
    ids, question_data, answer_data = generate_and_store_embeddings(collection=__collection__)
    load_data_to_mysql(__cursor__, __conn__,
                       TABLE_NAME, format_data(ids, question_data, answer_data))

    chatbot(collection=__collection__,
            **{"cursor": __cursor__, "conn": __conn__, "table_name": TABLE_NAME})
