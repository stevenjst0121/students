import os


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSJ_DATA_FILENAME = "jsj_data.xlsx"
ORDERS_DATA_FILENAME = "orders.xlsx"
RETURN_ORDERS_DATA_FILENAME = "return_orders.xlsx"
OUTPUT_FILENAME = "summary.xlsx"

# Source
DATA_PATH = os.path.join(ROOT_PATH, "data")
JSJ_DATA_FILEPATH = os.path.join(DATA_PATH, JSJ_DATA_FILENAME)
ORDERS_DATA_FILEPATH = os.path.join(DATA_PATH, ORDERS_DATA_FILENAME)
RETURN_ORDERS_DATA_FILEPATH = os.path.join(DATA_PATH, RETURN_ORDERS_DATA_FILENAME)
PICTURES_PATH = os.path.join(DATA_PATH, "pictures")

# Output
OUTPUT_PATH = os.path.join(ROOT_PATH, "out")
OUTPUT_FILEPATH = os.path.join(OUTPUT_PATH, OUTPUT_FILENAME)
OUTPUT_PATH_PICTURES = os.path.join(OUTPUT_PATH, "pictures")
