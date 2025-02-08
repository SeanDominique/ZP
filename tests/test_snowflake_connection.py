import snowflake.connector
import os
# Logging including the timestamp, thread and the source code location
import logging
from snowflake.connector.secret_detector import SecretDetector

# Using Python's Connector (which doesn't work, atm, with GCP regional endpoints)
logger_name = 'snowflake.connector'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)


ch = logging.FileHandler('/tmp/python_connector.log')
ch.setLevel(logging.DEBUG)
ch.setFormatter(SecretDetector('%(asctime)s - %(threadName)s %(filename)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(message)s'))
logger.addHandler(ch)


# print(os.getenv("SNOWFLAKE_PASSWORD"))
# print(os.getenv("SNOWFLAKE_USERNAME"))

ctx = snowflake.connector.connect(
    user= os.getenv("SNOWFLAKE_USERNAME"),
    password= os.getenv("SNOWFLAKE_PASSWORD"),
    account= os.getenv("SNOWFLAKE_ACCOUNT"),
    verify=False,
    login_timeout=120,
    network_timeout=120,
    socket_timeout=60
)

cs = ctx.cursor()

try:
    cs.execute("SELECT current_version()")
    one_row = cs.fetchone()
    print(one_row[0])

finally:
    cs.close()

ctx.close()
