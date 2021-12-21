import os
import sys
import logging

import pandas

# TODO
sys.path.append("/Users/sitengjin/dev/home/cathy/students")

from utils.excel_manager import ExcelReader, ExcelWriter
from utils.person import Person, Sex
from utils.logger import get_logger, setup_logging
from utils.validation import is_name_valid, is_id_valid
from utils.profile import Profile
from utils.constants import DATA_PATH, OUTPUT_PATH


# Constants
JSJ_DATA_FILENAME = "jsj_data.xlsx"
JSJ_DATA_FILEPATH = os.path.join(DATA_PATH, JSJ_DATA_FILENAME)
JSJ_DATA_FILENAME_FINAL = "jsj_data_final.xlsx"
OUTPUT_PATH_ID = os.path.join(OUTPUT_PATH, "id")
OUTPUT_PATH_NAME_ID = os.path.join(OUTPUT_PATH, "name_id")
JSJ_DATA_FILEPATH_FINAL_ID = os.path.join(OUTPUT_PATH_ID, JSJ_DATA_FILENAME_FINAL)
JSJ_DATA_FILEPATH_FINAL_NAME_ID = os.path.join(OUTPUT_PATH_NAME_ID, JSJ_DATA_FILENAME_FINAL)


class DataManager:
    def __init__(self):
        # Headers to read/write
        self.columns = [
            "序号",
            "姓名",
            "性别",
            "职业",
            "手机号",
            "微信昵称",
            "电子邮件",
            "身份证号码",
            "所在城市",
            "邮寄地址",
            "2寸蓝底照片",
        ]

        self.data = {}  # id -> person

        # metrics
        self.read_count = 0
        self.duplicate_count = 0
        self.invalid_count = 0

    def read_from_file(self, filepath):
        logger = get_logger()

        # Read excel
        reader = ExcelReader(filepath=filepath)
        df = reader.read()

        # Parse data
        for _, row in df.iterrows():
            self.read_count += 1
            try:
                name = row["姓名"]
                id = row["身份证号码"]
                profile_filename = row["2寸蓝底照片"]

                person = Person(
                    series=int(row["序号"]),
                    name=name,
                    sex=Sex.MALE if row["性别"] == "男" else Sex.FEMALE,
                    job=row["职业"],
                    mobile=int(row["手机号"]),
                    wechat=row["微信昵称"],
                    email=row["电子邮件"],
                    id=id,
                    city=row["所在城市"],
                    address=row["邮寄地址"],
                    profile=Profile(name, id, profile_filename),
                )

                # De-duplication
                if person.id in self.data:
                    old_series = self.data[person.id].series
                    if person.series > old_series:
                        logger.debug(
                            f"Overwriting duplicate record, old series={old_series}, "
                            f"new series={person.series}, {person}"
                        )
                    else:
                        logger.info(f"Dropping duplicate record, {person}")
                    self.duplicate_count += 1
                    continue
            except KeyError as e:
                logger.error(
                    f"Column name mismatch! Check whether the column names have been changed in {JSJ_DATA_FILENAME}."
                )
                raise e
            except Exception as e:
                logger.exception(e)

            # Data validation, only log error and continue
            if not is_name_valid(person.name):
                logger.error(f"[Data Validation] Invalid name, {person}")
                self.invalid_count += 1
            elif not is_id_valid(person.id):
                logger.error(f"[Data Validation] Invalid ID, {person}")
                self.invalid_count += 1
            else:
                self.data[person.id] = person

    def generate_output_files(self):
        self._mk_dir_if_not_exist(OUTPUT_PATH)

        # Generate jsj_data_final.xlsx
        # ID Only
        self._generate_xlsx_file(id_only=True)

        # Name + ID
        self._generate_xlsx_file(id_only=False)

    def _generate_xlsx_file(self, id_only: bool):
        if id_only:
            self._mk_dir_if_not_exist(OUTPUT_PATH_ID)
            writer = ExcelWriter(
                JSJ_DATA_FILEPATH_FINAL_ID, self._create_dataframe_from_data(id_only)
            )
        else:
            self._mk_dir_if_not_exist(OUTPUT_PATH_NAME_ID)
            writer = ExcelWriter(
                JSJ_DATA_FILEPATH_FINAL_NAME_ID, self._create_dataframe_from_data(id_only)
            )
        writer.write()

    def _create_dataframe_from_data(self, id_only: bool):
        df = pandas.DataFrame(columns=self.columns)
        for _, person in self.data.items():
            row = {
                "序号": person.series,
                "姓名": person.name,
                "性别": "女" if person.sex == Sex.FEMALE else "男",
                "职业": person.job,
                "手机号": person.mobile,
                "微信昵称": person.wechat,
                "电子邮件": person.email,
                "身份证号码": person.id,
                "所在城市": person.city,
                "邮寄地址": person.address,
                "2寸蓝底照片": (
                    person.profile.id_filename if id_only else person.profile.name_id_filename
                ),
            }
            df = df.append(row, ignore_index=True)
        return df

    def _mk_dir_if_not_exist(self, path):
        logger = get_logger()

        if not os.path.isdir(path):
            logger.info(f"Creating directory {path}")
            os.mkdir(path)

    def log_read_summary(self):
        logger = get_logger()

        logger.info("==================Summary==================")
        logger.info(f"Total record parsed: {self.read_count}")
        logger.info(f"Total valid records: {len(self.data)}")

        logger.debug("------------------All Valid Records------------------")
        for _, person in self.data.items():
            logger.debug(person)
        logger.debug("------------------All Valid Records------------------")

        logger.info(f"Total invalid records: {self.invalid_count}")
        logger.info(f"Dropped duplicate records: {self.duplicate_count}")
        logger.info("==================Summary==================")


def run():
    logger = get_logger()

    # Initialize Data Manager
    data_manager = DataManager()
    data_manager.read_from_file(JSJ_DATA_FILEPATH)
    data_manager.log_read_summary()

    # Generate Output Files
    data_manager.generate_output_files()


if __name__ == "__main__":
    setup_logging()
    sys.exit(run())
