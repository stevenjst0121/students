from utils.logger import get_logger
from utils.excel_manager import ExcelReader
from utils.person import Person, Sex
from utils.profile import Profile
from utils.validation import is_id_valid, is_name_valid, is_mobile_valid


class JSJDataManager:
    def __init__(self):
        self.data = {}  # id -> person
        self.id_by_order_id = {}  # order_id -> id
        self.id_by_mobile = {}  # mobile -> id

        # metrics
        self.read_count = 0
        self.duplicate_count = 0
        self.invalid_count = 0

    def read_from_file(self, filepath):
        logger = get_logger()
        logger.info(f"Reading JSJ data from {filepath}")

        # Read excel
        reader = ExcelReader(filepath=filepath)
        df = reader.read()

        # Parse data
        for _, row in df.iterrows():
            self.read_count += 1
            try:
                name = row["姓名"]
                id = row["身份证号码"]
                mobile_str = str(row["手机号"])
                profile_filename = str(row["2寸蓝底照片"]) if not row.isnull()["2寸蓝底照片"] else None
                order_id_20_str = str(row["20位订单编号"])

                person = Person(
                    series=row["序号"],
                    name=name,
                    sex=Sex.MALE if row["性别"] == "男" else Sex.FEMALE,
                    job=row["职业"],
                    mobile=int(mobile_str) if mobile_str.isdigit() else None,
                    wechat=row["微信昵称"],
                    email=row["电子邮件"],
                    id=id,
                    city=row["所在城市"],
                    address=row["邮寄地址"],
                    order_id_20=int(order_id_20_str) if order_id_20_str.isdigit() else None,
                    profile=Profile(name, id, profile_filename),
                )

                # Data validation
                if not is_name_valid(person.name):
                    logger.error(f"[Data Validation] Invalid name, skipping. {person}")
                    self.invalid_count += 1
                    continue
                elif not is_id_valid(person.id):
                    logger.error(f"[Data Validation] Invalid ID, skipping. {person}")
                    self.invalid_count += 1
                    continue
                elif not is_mobile_valid(person.mobile):
                    logger.warning(f"[Data Validation] Invalid mobile, NOT skipping. {person}")

                # De-duplication
                if person.id in self.data:
                    self.duplicate_count += 1
                    old_series = self.data[person.id].series
                    if person.series > old_series and person.profile.is_valid():
                        logger.info(
                            f"Overwriting duplicate record, old series={old_series}, "
                            f"new series={person.series}, {person}"
                        )
                    else:
                        logger.info(f"Dropping duplicate record, {person}")
                        continue

                # Writing person to data
                self.data[person.id] = person
                if person.order_id_20 is not None:
                    self.id_by_order_id[person.order_id_20] = person.id
                if person.mobile is not None:
                    self.id_by_mobile[person.mobile] = person.id

            except KeyError as e:
                logger.error(
                    f"Column name mismatch! Check whether the column names have been changed in {filepath}."
                )
                raise e
            except Exception as e:
                logger.exception(e)
                raise e

        self.log_read_summary()

    def log_read_summary(self):
        logger = get_logger()

        logger.info("==================JSJ Data Manager Summary==================")
        logger.info(f"Total record parsed: {self.read_count}")
        logger.info(f"Total valid records: {len(self.data)}")

        logger.debug("------------------All Valid Records------------------")
        for _, person in self.data.items():
            logger.debug(person)
        logger.debug("------------------All Valid Records------------------")

        logger.info(f"Total invalid records: {self.invalid_count}")
        logger.info(f"Dropped duplicate records: {self.duplicate_count}")
        logger.info("==================JSJ Data Manager Summary==================")
