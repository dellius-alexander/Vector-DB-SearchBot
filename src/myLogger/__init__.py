import json
import os
import logging.config
import logging


LOGGING_CONFIG = "../Resources/logging.json"
print(f"Logging config: {LOGGING_CONFIG}")

# check if logging.json has been loaded
if not logging.root.handlers:
    if not os.path.exists("logs"):
        os.mkdir("logs")
    # log_config = [f for f in log_json if os.path.exists(f)][0]
    with open(LOGGING_CONFIG) as file:
        data = json.load(file)
        print(data)
    # read initial config file
    logging.config.dictConfig(config=data)
    # CustomConfig(config=data)
    # # create and start listener on port 9999
    # t = logging.config.listen(int(os.getenv('PORT')))
    # t.start()
#     log = logging.getLogger(__name__)
# else:
#     log = logging.getLogger(__name__)
