from pymilvus import Collection
import gradio as gr

from milvus.question_answering import connect_to_milvus_and_mysql, create_collection, create_table_in_mysql, \
    load_data_to_mysql, generate_and_store_embeddings, format_data, handle_diff
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
        inputs=gr.Textbox(
            label="Query Search",
            info="Ask me Question and Press Submit",
            lines=3,

        ),
        outputs=gr.HighlightedText(
            label="Diff",
            combine_adjacent=True,
            show_legend=True,
        ).style(color_map={"+": "red", "-": "green"}),
        theme=gr.themes.Base(),
        description="This is a simple question and answering system that uses a corpus of 1000 questions and answers.",
        info=gr.Markdown(about)
    )

    demo.launch(share=False)


if __name__ == '__main__':
    __conn__, __cursor__, collection = connect_to_milvus_and_mysql()
    __collection__ = create_collection(TABLE_NAME)
    create_table_in_mysql(__cursor__, TABLE_NAME)
    ids, question_data, answer_data = generate_and_store_embeddings(collection=__collection__)
    load_data_to_mysql(__cursor__, __conn__, TABLE_NAME, format_data(ids, question_data, answer_data))

    chatbot(collection=__collection__,
            **{"cursor": __cursor__, "conn": __conn__, "table_name": TABLE_NAME})
