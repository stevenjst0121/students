from utils.logger import get_logger
from utils.excel_manager import ExcelReader
from utils.return_order import ReturnOrder


class ReturnOrdersDataManager:
    def __init__(self):
        self.data = {}  # order ID -> Order

        # metrics
        self.read_count = 0
        self.duplicate_count = 0
        self.invalid_count = 0

    def read_from_file(self, filepath):
        logger = get_logger()
        logger.info(f"Reading return orders data from {filepath}")

        # Read Excel
        reader = ExcelReader(filepath)
        df = reader.read()

        # Parse Data
        for _, row in df.iterrows():
            self.read_count += 1
            try:
                return_order = ReturnOrder(
                    order_id=int(row["订单编号"]),
                    price=float(row["供应商成本/件"]),
                    name=row["收货人姓名"],
                    receipt_mobile=int(row["收货人手机"]),
                    attend_mobile=int(row["听课手机号"]),
                    address=row["总地址"],
                )

                # De-duplication
                if return_order.order_id in self.data:
                    logger.error(
                        f"Duplicate return order record found, overwriting. {return_order}"
                    )
                    self.duplicate_count += 1

                self.data[return_order.order_id] = return_order
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

        logger.info("==================Return Orders Data Manager Summary==================")
        logger.info(f"Total record parsed: {self.read_count}")
        logger.info(f"Total valid records: {len(self.data)}")

        logger.debug("------------------All Valid Records------------------")
        for _, order in self.data.items():
            logger.debug(order)
        logger.debug("------------------All Valid Records------------------")

        logger.info(f"Total invalid records: {self.invalid_count}")
        logger.info(f"Dropped duplicate records: {self.duplicate_count}")
        logger.info("==================Return Orders Data Manager Summary==================")
