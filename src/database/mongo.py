import json
import traceback
from mongoengine import connect, ConnectionFailure
import os

# Get the logger
from ..myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)

# Get the port from the environment variables
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "root")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "developer")
log.info("MONGODB_USERNAME: %s" % MONGODB_USERNAME)
log.info("MONGODB_PASSWORD: %s" % MONGODB_PASSWORD)
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "admin")
MONGODB_HOST = os.getenv("MONGODB_HOST", "0.0.0.0")
MONGODB_PORT = os.getenv("MONGODB_PORT", 27017)


class MongoDB(connect, ConnectionFailure):
    db = os.getenv("MONGODB_DATABASE", "admin")
    host = os.getenv("MONGODB_HOST", "0.0.0.0")
    port = os.getenv("MONGODB_PORT", 27017)
    username = os.getenv("MONGODB_USERNAME", "root")
    password = os.getenv("MONGODB_PASSWORD", "developer")

    def __init__(self,  # the name of the database to use, for compatibility with connect
                 db=MONGODB_DATABASE,
                 # the host name of the: program: mongod instance to connect to
                 # f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}",
                 host=f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}",
                 # the name that will be used to refer to this connection throughout MongoEngine
                 alias="default",
                 # the name of the specific database to use
                 name=MONGODB_DATABASE,
                 # the port that the: program: mongod instance is running on
                 port=int(MONGODB_PORT),
                 # # The read preference for the collection
                 # read_preference=None,
                 # username to authenticate with
                 username=MONGODB_USERNAME,
                 # password to authenticate with
                 password=MONGODB_PASSWORD,
                 # database to authenticate against
                 authentication_source="admin",
                 # # database authentication mechanisms. By default, use SCRAM-SHA-1 with MongoDB 3.0 and later,
                 # # MONGODB-CR (MongoDB Challenge Response protocol) for older servers.
                 # authentication_mechanism=None,
                 # # using alternative connection client other than pymongo.MongoClient, e.g. mongomock, montydb,
                 # # that provides pymongo alike interface but not necessarily for connecting to a real mongo instance.
                 # mongo_client_class=None,
                 # # ad-hoc parameters to be passed into the pymongo driver, for example maxpoolsize, tz_aware, etc.
                 # # See the documentation for pymongo’s MongoClient for a full list.
                 # kwargs=None,
                 **kwargs):
        self.client = super().__init__(db=db,
                                       host=host or self.host,
                                       port=port or self.port,
                                       username=username or self.username,
                                       password=password or self.password)
        self.alias = alias
        self.name = name
        self.kwargs = kwargs

    def __str__(self):
        return f"MongoDB(db={self.db}, host={self.host}, port={self.port}, username={self.username}, password={self.password})"

    def __repr__(self):
        return f"MongoDB(db={self.db}, host={self.host}, port={self.port}, username={self.username}, password={self.password})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __lt__(self, other):
        return self.__dict__ < other.__dict__

    def __le__(self, other):
        return self.__dict__ <= other.__dict__

    def __gt__(self, other):
        return self.__dict__ > other.__dict__

    def __ge__(self, other):
        return self.__dict__ >= other.__dict__

    def __hash__(self):
        return hash(self.__dict__)

    def health_check(self):
        try:
            self.client.admin.command("ismaster")
            return True
        except ConnectionFailure:
            return False

    def ping_db(self):
        try:
            self.client.admin.command("ping")
            return True
        except ConnectionFailure:
            return False

    def get_db(self):
        return self.client[self.db]


def connect_to_mongo():
    try:
        client = connect(
            # the name of the database to use, for compatibility with connect
            db=MONGODB_DATABASE,
            # the host name of the: program: mongod instance to connect to
            # f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}",
            host=f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}",
            # the name that will be used to refer to this connection throughout MongoEngine
            alias="default",
            # the name of the specific database to use
            name=MONGODB_DATABASE,
            # the port that the: program: mongod instance is running on
            port=int(MONGODB_PORT),
            # # The read preference for the collection
            # read_preference=None,
            # username to authenticate with
            username=MONGODB_USERNAME,
            # password to authenticate with
            password=MONGODB_PASSWORD,
            # database to authenticate against
            authentication_source="admin",
            # # database authentication mechanisms. By default, use SCRAM-SHA-1 with MongoDB 3.0 and later,
            # # MONGODB-CR (MongoDB Challenge Response protocol) for older servers.
            # authentication_mechanism=None,
            # # using alternative connection client other than pymongo.MongoClient, e.g. mongomock, montydb,
            # # that provides pymongo alike interface but not necessarily for connecting to a real mongo instance.
            # mongo_client_class=None,
            # # ad-hoc parameters to be passed into the pymongo driver, for example maxpoolsize, tz_aware, etc.
            # # See the documentation for pymongo’s MongoClient for a full list.
            # kwargs=None,
        )
        if client:
            log.info("Connected to MongoDB successfully.")
            log.info(f"MongoDB connection: {client}")
            result = client.admin.command("ping")
            if result:
                log.info(f"MongoDB ping result: {result}")
                # create new users: alpha and beta

            else:
                log.error("Could not ping MongoDB.")
        else:
            log.error("Could not connect to MongoDB.")
        # The ping command is cheap and does not require auth.
        return client
    except ConnectionFailure as e:
        log.error("Server not available.")
        log.error(e, exc_info=traceback.format_exc(), stack_info=True)
    except Exception as e:
        log.error("Error initializing the database.")
        log.error(e, exc_info=traceback.format_exc(), stack_info=True)
