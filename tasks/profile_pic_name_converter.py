import os
import sys
import shutil

import pandas

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import get_logger, setup_logging
from utils.constants import *
from utils.jsj_data_manager import JSJDataManager
from utils.orders_data_manager import OrdersDataManager
from utils.return_orders_data_manager import ReturnOrdersDataManager
from utils.excel_manager import ExcelWriter


class TaskManager:
    def __init__(self):
        # Headers to read/write
        self.columns = ["订单号", "姓名", "手机", "身份证", "照片"]

        self.jsj_data_manager = JSJDataManager()
        self.orders_data_manager = OrdersDataManager()
        self.return_orders_data_manager = ReturnOrdersDataManager()

    def load(self):
        self.jsj_data_manager.read_from_file(JSJ_DATA_FILEPATH)
        self.orders_data_manager.read_from_file(ORDERS_DATA_FILEPATH)
        self.return_orders_data_manager.read_from_file(RETURN_ORDERS_DATA_FILEPATH)

    def generate_output_files(self):
        output_data = self._generate_output_data()
        self._write_output_files(output_data)
        self._copy_profile_files(output_data)

    def _generate_output_data(self):
        logger = get_logger()

        # Filter by orders
        order_ids = []
        returned_orders_count = 0
        for order_id, order in self.orders_data_manager.data.items():
            if order_id not in self.return_orders_data_manager.data and order.price > 0.01:
                order_ids.append(order_id)
            else:
                returned_orders_count += 1
        order_ids.sort()

        logger.info("==================Order Filter Summary==================")
        logger.info(f"Total number of orders: {len(self.orders_data_manager.data)}")
        logger.info(f"Number of returned orders: {returned_orders_count}")
        logger.info(f"Number of filtered orders: {len(order_ids)}")
        logger.info("==================Order Filter Summary==================")

        output_data = []
        for order_id in order_ids:
            # Match order_id to person
            # 1. Try to match by order_id_20
            # 2. Try to match by order.attend_mobile
            # 3. Try to match by order.receipt_mobile
            # 4. If no such person found, set to None
            order = self.orders_data_manager.data[order_id]
            order_id_20 = order.order_id_20
            attend_mobile = order.attend_mobile
            receipt_mobile = order.receipt_mobile
            person = None
            if order_id_20 in self.jsj_data_manager.id_by_order_id:
                person = self.jsj_data_manager.data[
                    self.jsj_data_manager.id_by_order_id[order_id_20]
                ]
            elif attend_mobile is not None and attend_mobile in self.jsj_data_manager.id_by_mobile:
                person = self.jsj_data_manager.data[
                    self.jsj_data_manager.id_by_mobile[attend_mobile]
                ]
            elif (
                receipt_mobile is not None and receipt_mobile in self.jsj_data_manager.id_by_mobile
            ):
                person = self.jsj_data_manager.data[
                    self.jsj_data_manager.id_by_mobile[receipt_mobile]
                ]

            output_data.append((order, person))

        return output_data

    def _write_output_files(self, output_data):
        df = pandas.DataFrame(columns=self.columns)

        for order, person in output_data:
            # Add person to row
            row = {
                "订单号": str(order.order_id_20),  # hack, pandas does not support 64-bit usigned int
                "姓名": person.name if person is not None else None,
                "手机": person.mobile if person is not None else None,
                "身份证": person.id if person is not None else None,
                "照片": person.profile.raw_filename if person is not None else None,
            }
            df = df.append(row, ignore_index=True)

        self._mk_dir_if_not_exist(OUTPUT_PATH)
        writer = ExcelWriter(OUTPUT_FILEPATH, df)
        writer.write()

    def _mk_dir_if_not_exist(self, path):
        logger = get_logger()

        if not os.path.isdir(path):
            logger.info(f"Creating directory {path}")
            os.mkdir(path)

    def _copy_profile_files(self, output_data):
        logger = get_logger()

        self._mk_dir_if_not_exist(OUTPUT_PATH_PICTURES)
        for _, person in output_data:
            if person is None:
                continue

            profile = person.profile

            # THIS IS BAD
            # Hard-coded logic to skip copying if there is no profile picture
            if not profile.is_valid():
                continue

            src_file_path = os.path.join(PICTURES_PATH, profile.raw_filename)
            dst_file_path = os.path.join(OUTPUT_PATH_PICTURES, profile.id_filename)
            try:
                shutil.copyfile(src=src_file_path, dst=dst_file_path)
            except Exception as e:
                logger.exception(e)


def run():
    # Initialize Task Manager
    data_manager = TaskManager()
    data_manager.load()

    # Generate Output Files
    data_manager.generate_output_files()


if __name__ == "__main__":
    setup_logging()
    sys.exit(run())
