import os


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSJ_DATA_FILENAME = "jsj_data.xlsx"
JSJ_DATA_FILENAME_FINAL = "jsj_data_final.xlsx"

# Source
DATA_PATH = os.path.join(ROOT_PATH, "data")
JSJ_DATA_FILEPATH = os.path.join(DATA_PATH, JSJ_DATA_FILENAME)
PICTURES_PATH = os.path.join(DATA_PATH, "pictures")

# Output
OUTPUT_PATH = os.path.join(ROOT_PATH, "out")
OUTPUT_PATH_ID = os.path.join(OUTPUT_PATH, "id")
OUTPUT_PATH_NAME_ID = os.path.join(OUTPUT_PATH, "name_id")

#   ID
JSJ_DATA_FILEPATH_FINAL_ID = os.path.join(OUTPUT_PATH_ID, JSJ_DATA_FILENAME_FINAL)
OUTPUT_PATH_ID_PICTURES = os.path.join(OUTPUT_PATH_ID, "pictures")

#   Name+ID
JSJ_DATA_FILEPATH_FINAL_NAME_ID = os.path.join(OUTPUT_PATH_NAME_ID, JSJ_DATA_FILENAME_FINAL)
OUTPUT_PATH_NAME_ID_PICTURES = os.path.join(OUTPUT_PATH_NAME_ID, "pictures")
