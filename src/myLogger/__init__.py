import json
import os
import logging.config
import logging


def find_src_path(path=os.getcwd()):
    try:
        print(f"Path: {path}")
        if path.split('/')[-1] == 'src' and os.path.exists(path):
            return path
        elif os.path.exists(f"{path}/src"):
            return os.path.join(path, "src")
        path = "/".join(os.path.dirname(path).split("/")[0:-1])
        return find_src_path(path)
    except Exception as e:
        print(e)
        return None


def clean_log_dir(path):
    """
    Clean log directory: reduce the log directory to 10 files
    :param path: log directory path
    """
    try:
        files = os.listdir(path)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))
        if len(files) > 10:
            for file in files[0:-10]:
                os.remove(os.path.join(path, file))
    except Exception as e:
        print(e)


working_dir = find_src_path(os.getcwd())
logging_config = f"{working_dir}/Resources/logging.json"
print(f"Logging config: {logging_config}")
print(f"Current Working directory: {working_dir}")
# check if logging.json has been loaded
if not logging.root.handlers:
    if not os.path.exists(f"{working_dir}/logs"):
        os.mkdir(f"{working_dir}/logs")
    # log_config = [f for f in log_json if os.path.exists(f)][0]
    with open(logging_config) as file:
        data = json.load(file)
        print(data)
    clean_log_dir(f"{working_dir}/logs")
    # read initial config file
    logging.config.dictConfig(config=data)
    # CustomConfig(config=data)
    # # create and start listener on port 9999
    # t = logging.config.listen(int(os.getenv('PORT')))
    # t.start()
#     log = logging.getLogger(__name__)
# else:
#     log = logging.getLogger(__name__)


