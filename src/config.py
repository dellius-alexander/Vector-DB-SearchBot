import dotenv
import os

from sentence_transformers import SentenceTransformer

# Load environment variables
dotenv.load_dotenv(
    dotenv_path=os.path.join(os.getcwd(), ".env")
                or dotenv.find_dotenv(".env", False, False),
    verbose=True,
    encoding="utf-8",
)

dotenv.find_dotenv(".env")

# Application Configuration Options
APP_NAME = os.getenv("APP_NAME", "question_answering")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = os.getenv("APP_PORT", "8000")
APP_SOURCE = os.getenv("APP_SOURCE", ".").strip()
APP_LOG_LEVEL = os.getenv("APP_LOG_LEVEL", True)

# MySQL Configuration Options
MYSQL_HOST = os.getenv("MYSQL_HOST", "0.0.0.0")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "milvus")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "developer")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "milvus_meta")
MYSQL_DATABASE_TABLE_NAME = os.getenv("MYSQL_DATABASE_TABLE_NAME", "question_answering")

# Milvus Configuration Options
MILVUS_USER = os.getenv("MILVUS_USER", "milvus")
MILVUS_PASSWORD = os.getenv("MILVUS_PASSWORD", "developer")
MILVUS_HOST = os.getenv("MILVUS_HOST", "0.0.0.0")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
MILVUS_COLLECTION = os.getenv("MILVUS_COLLECTION", "question_answering")
MILVUS_CONNECTION_ALIAS = os.getenv("MILVUS_CONNECTION_ALIAS", "default")
MILVUS_DIMENSION = os.getenv("MILVUS_DIMENSION", 768)
MILVUS_INDEX_FILE_SIZE = os.getenv("MILVUS_INDEX_FILE_SIZE", 1024)
MILVUS_METRIC_TYPE = os.getenv("MILVUS_METRIC_TYPE", "L2")
MILVUS_INDEX_TYPE = os.getenv("MILVUS_INDEX_TYPE", "IVF_FLAT")
MILVUS_NLIST = os.getenv("MILVUS_NLIST", 16384)
MILVUS_TOP_K = os.getenv("MILVUS_TOP_K", 10)
MILVUS_SEARCH_PARAM = {"nprobe": 16}
# Milvus Timeout Configuration Options
MILVUS_TIMEOUT = 60
MILVUS_SEARCH_TIMEOUT = 60
MILVUS_INSERT_TIMEOUT = 60
MILVUS_UPSERT_TIMEOUT = 60
MILVUS_CREATE_TIMEOUT = 60
MILVUS_DROP_TIMEOUT = 60
MILVUS_HAS_TIMEOUT = 60
MILVUS_DELETE_TIMEOUT = 60
MILVUS_LOAD_TIMEOUT = 60
MILVUS_RELEASE_TIMEOUT = 60
MILVUS_FLUSH_TIMEOUT = 60
MILVUS_COMPACT_TIMEOUT = 60
MILVUS_GET_TIMEOUT = 60
MILVUS_COUNT_TIMEOUT = 60
MILVUS_GET_PARTITION_STATS_TIMEOUT = 60
MILVUS_GET_COLLECTION_STATS_TIMEOUT = 60
MILVUS_CALCULATE_DISTANCE_TIMEOUT = 60

# Dataset Configuration Options
DATASET_PATH = os.getenv("DATASET_PATH", f'{os.getcwd()}/Resources/datasets/questions_answers.csv')
DATASET_NAME = os.getenv("DATASET_NAME", "questions_answers")

# Models Configuration Options
MODEL_SELECTION = dict(
    {"sentence_transformers": SentenceTransformer('all-mpnet-base-v2')}
)
