import os
import sys
import logging

# TODO
sys.path.append("/Users/sitengjin/dev/home/cathy/students")

from utils.excel_manager import ExcelReader
from utils.person import Person, Sex
from utils.logger import get_logger, setup_logging
from utils.validation import is_name_valid, is_id_valid
from utils.profile import Profile
from utils.constants import DATA_PATH


# Constants
JSJ_DATA_FILENAME = "jsj_data.xlsx"
JSJ_DATA_FILEPATH = os.path.join(DATA_PATH, JSJ_DATA_FILENAME)


def run():
    logger = get_logger()

    # Read excel
    reader = ExcelReader(filepath=JSJ_DATA_FILEPATH)
    df = reader.read()

    # Parse data
    data = {}  # id -> Person
    count = 0
    duplicate_count = 0
    invalid_count = 0
    for _, row in df.iterrows():
        count += 1
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
            if person.id in data:
                old_series = data[person.id].series
                if person.series > old_series:
                    logger.debug(
                        f"Overwriting duplicate record, old series={old_series}, "
                        f"new series={person.series}, {person}"
                    )
                else:
                    logger.info(f"Dropping duplicate record, {person}")
                duplicate_count += 1
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
            invalid_count += 1
        elif not is_id_valid(person.id):
            logger.error(f"[Data Validation] Invalid ID, {person}")
            invalid_count += 1
        else:
            data[person.id] = person

    # Summary
    logger.info("==================Summary==================")
    logger.info(f"Total record parsed: {count}")
    logger.info(f"Total valid records: {len(data)}")

    logger.debug("------------------All Valid Records------------------")
    for _, person in data.items():
        logger.debug(person)
    logger.debug("------------------All Valid Records------------------")

    logger.info(f"Total invalid records: {invalid_count}")
    logger.info(f"Dropped duplicate records: {duplicate_count}")
    logger.info("==================Summary==================")


if __name__ == "__main__":
    setup_logging()
    sys.exit(run())
