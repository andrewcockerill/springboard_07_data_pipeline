from utils import get_db_connection, load_third_party, query_popular_tickets
import mysql.connector
import logging

# Constants
FILE_PATH = '../data/third_party_sales_1.csv'

# Logging
logger = logging.getLogger('db_setup')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('../logs/app.log')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.info('application started')

# Get connection object
logger.info('requesting connection object')
conn = get_db_connection()
logger.info('obtained connection object')

# Fetch data and run query
try:
    # Build database
    logger.info('loading third party data')
    load_third_party(conn, FILE_PATH)
    logger.info('loaded third party data')

    # Query
    logger.info('Running query')
    query_popular_tickets(conn)
    logger.info('Query complete')
except Exception as e:
    logger.error(e)
finally:
    conn.close()