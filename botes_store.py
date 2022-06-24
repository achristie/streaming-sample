import sqlite3


CREATE_TABLE = """
  CREATE TABLE IF NOT EXISTS botes
    (
      BUYER text,
      BUYER_MNEMONIC text,
      BUYER_PARENT text,
      C1_BASIS_PERIOD text,
      C1_BASIS_PERIOD_DETAILS text,
      C1_PERCENTAGE text,
      C1_PRICE int,
      C1_PRICE_BASIS text,
      C2_BASIS_PERIOD text,
      C2_BASIS_PERIOD_DETAILS text,
      C2_PERCENTAGE text,
      C2_PRICE int,
      C2_PRICE_BASIS text,
      C3_BASIS_PERIOD text,
      C3_BASIS_PERIOD_DETAILS text,
      C3_PERCENTAGE text,
      C3_PRICE int,
      C3_PRICE_BASIS text,
      COUNTERPARTY text,
      COUNTERPARTY_MNEMONIC text,
      COUNTERPARTY_PARENT text,
      DEAL_BEGIN datetime,
      DEAL_END datetime,
      DEAL_ID int,
      DEAL_QUANTITY int,
      DEAL_QUANTITY_MAX int,
      DEAL_QUANTITY_MIN int,
      DEAL_TERMS text,
      HUB text,
      LEG_PRICES text,
      LOT_SIZE int,
      LOT_UNIT text,
      MARKET text,
      MARKET_MAKER text,
      MARKET_MAKER_MNEMONIC text,
      MARKET_MAKER_PARENT text,
      MARKET_SHORT_CODE text,
      MARKET_TYPE text,
      OCO_ORDER_ID text,
      ORDER_BEGIN datetime,
      ORDER_CANCELLED text,
      ORDER_CLASSIFICATION text,
      ORDER_DATE text,
      ORDER_DERIVED text,
      ORDER_END datetime,
      ORDER_ID int,
      ORDER_PLATTS_ID int,
      ORDER_QUANTITY int,
      ORDER_QUANTITY_TOTAL int,
      ORDER_REPEAT text,
      ORDER_SEQUENCE int,
      ORDER_SPREAD text,
      ORDER_STATE text,
      ORDER_STATE_DETAIL text,
      ORDER_TIME text,
      ORDER_TYPE text,
      PARENT_DEAL_ID int,
      PRICE num,
      PRICE_UNIT text,
      PRODUCT text,
      REFERENCE_ORDER_ID int,
      SELLER text,
      SELLER_MNEMONIC text,
      SELLER_PARENT text,
      STRIP text,
      UPDATE_TIME datetime,
      WINDOW_REGION text,
      WINDOW_STATE text
    )
"""


class Db:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    def create_table(self):
        self.cursor.execute(CREATE_TABLE)
