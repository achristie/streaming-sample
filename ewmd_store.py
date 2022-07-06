import sqlite3

INSERT_RECORD = """
    INSERT INTO ewmd(
        buyer, buyer_mnemonic, buyer_parent, c1_basis_period, c1_basis_period_details, c1_percentage, c1_price, c1_price_basis,
        c2_basis_period, c2_basis_period_details , c2_percentage , c2_price , c2_price_basis , c3_basis_period ,
        c3_basis_period_details , c3_percentage , c3_price , c3_price_basis , counterparty , counterparty_mnemonic , counterparty_parent ,
        deal_begin , deal_end , deal_id , deal_quantity ,
        deal_quantity_max , deal_quantity_min , deal_terms , hub , leg_prices , lot_size , lot_unit , market ,
        market_maker , market_maker_mnemonic , market_maker_parent , market_short_code, market_type , oco_order_id , order_begin , order_cancelled ,
        order_classification , order_date , order_derived , order_end , order_id , order_platts_id , order_quantity , order_quantity_total , order_repeat ,
        order_sequence , order_spread , order_state , order_state_detail , order_time , order_type , parent_deal_id , price ,
        price_unit , product , reference_order_id , seller , seller_mnemonic , seller_parent , strip , update_time ,
        window_region , window_state 
      ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?)
"""

CREATE_TABLE = """
  CREATE TABLE IF NOT EXISTS ewmd
    (
      buyer text,
      buyer_mnemonic text,
      buyer_parent text,
      c1_basis_period text,
      c1_basis_period_details text,
      c1_percentage text,
      c1_price int,
      c1_price_basis text,
      c2_basis_period text,
      c2_basis_period_details text,
      c2_percentage text,
      c2_price int,
      c2_price_basis text,
      c3_basis_period text,
      c3_basis_period_details text,
      c3_percentage text,
      c3_price int,
      c3_price_basis text,
      counterparty text,
      counterparty_mnemonic text,
      counterparty_parent text,
      deal_begin datetime,
      deal_end datetime,
      deal_id int,
      deal_quantity int,
      deal_quantity_max int,
      deal_quantity_min int,
      deal_terms text,
      hub text,
      leg_prices text,
      lot_size int,
      lot_unit text,
      market text,
      market_maker text,
      market_maker_mnemonic text,
      market_maker_parent text,
      market_short_code text,
      market_type text,
      oco_order_id text,
      order_begin datetime,
      order_cancelled text,
      order_classification text,
      order_date text,
      order_derived text,
      order_end datetime,
      order_id int,
      order_platts_id int,
      order_quantity int,
      order_quantity_total int,
      order_repeat text,
      order_sequence int,
      order_spread text,
      order_state text,
      order_state_detail text,
      order_time text,
      order_type text,
      parent_deal_id int,
      price num,
      price_unit text,
      product text,
      reference_order_id int,
      seller text,
      seller_mnemonic text,
      seller_parent text,
      strip text,
      update_time datetime,
      window_region text,
      window_state text
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

    def insert(self, bot):
        self.cursor.execute(
            INSERT_RECORD,
            (
                bot.get("BUYER"),
                bot.get("BUYER_MNEMONIC"),
                bot.get("BUYER_PARENT"),
                bot.get("C1_BASIS_PERIOD"),
                bot.get("C1_BASIS_PERIOD_DETAILS"),
                bot.get("C1_PERCENTAGE"),
                bot.get("C1_PRICE"),
                bot.get("C1_PRICE_BASIS"),
                bot.get("C2_BASIS_PERIOD"),
                bot.get("C2_BASIS_PERIOD_DETAILS"),
                bot.get("C2_PERCENTAGE"),
                bot.get("C2_PRICE"),
                bot.get("C2_PRICE_BASIS"),
                bot.get("C3_BASIS_PERIOD"),
                bot.get("C3_BASIS_PERIOD_DETAILS"),
                bot.get("C3_PERCENTAGE"),
                bot.get("C3_PRICE"),
                bot.get("C3_PRICE_BASIS"),
                bot.get("COUNTERPARTY"),
                bot.get("COUNTERPARTY_MNEMONIC"),
                bot.get("COUNTERPARTY_PARENT"),
                bot.get("DEAL_BEGIN"),
                bot.get("DEAL_END"),
                bot.get("DEAL_ID"),
                bot.get("DEAL_QUANTITY"),
                bot.get("DEAL_QUANTITY_MAX"),
                bot.get("DEAL_QUANTITY_MIN"),
                bot.get("DEAL_TERMS"),
                bot.get("HUB"),
                bot.get("LEG_PRICES"),
                bot.get("LOT_SIZE"),
                bot.get("LOT_UNIT"),
                bot.get("MARKET"),
                bot.get("MARKET_MAKER"),
                bot.get("MARKET_MAKER_MNEMONIC"),
                bot.get("MARKET_MAKER_PARENT"),
                bot.get("MARKET_SHORT_CODE"),
                bot.get("MARKET_TYPE"),
                bot.get("OCO_ORDER_ID"),
                bot.get("ORDER_BEGIN"),
                bot.get("ORDER_CANCELLED"),
                bot.get("ORDER_CLASSIFICATION"),
                bot.get("ORDER_DATE"),
                bot.get("ORDER_DERIVED"),
                bot.get("ORDER_END"),
                bot.get("ORDER_ID"),
                bot.get("ORDER_PLATTS_ID"),
                bot.get("ORDER_QUANTITY"),
                bot.get("ORDER_QUANTITY_TOTAL"),
                bot.get("ORDER_REPEAT"),
                bot.get("ORDER_SEQUENCE"),
                bot.get("ORDER_SPREAD"),
                bot.get("ORDER_STATE"),
                bot.get("ORDER_STATE_DETAIL"),
                bot.get("ORDER_TIME"),
                bot.get("ORDER_TYPE"),
                bot.get("PARENT_DEAL_ID"),
                bot.get("PRICE"),
                bot.get("PRICE_UNIT"),
                bot.get("PRODUCT"),
                bot.get("REFERENCE_ORDER_ID"),
                bot.get("SELLER"),
                bot.get("SELLER_MNEMONIC"),
                bot.get("SELLER_PARENT"),
                bot.get("STRIP"),
                bot.get("UPDATE_TIME"),
                bot.get("WINDOW_REGION"),
                bot.get("WINDOW_STATE"),
            ),
        )
        self.connection.commit()
