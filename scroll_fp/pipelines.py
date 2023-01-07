# useful for handling different item types with a single interface
import pg8000
import json
import logging
import os
from dotenv import load_dotenv  # for python-dotenv method
load_dotenv()  # for python-dotenv method

class PostgresPipeline(object):
    # Init
    user = os.environ.get('user')
    password = os.environ.get('password')
    host = os.environ.get('host')
    database = os.environ.get('database')
    port = os.environ.get('port')
    schema = os.environ.get('schema')
    insert_table = os.environ.get('insert_table')

    def open_spider(self, spider):
        self.client = pg8000.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
            port=self.port)
        self.curr = self.client.cursor()

    def close_spider(self, spider):
       self.client.close()

    def process_item(self, item, spider):

        # Create table to insert
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS {schema}.{insert_table} (
                utc_time timestamp,
                crawl_ts integer,
                barcode text,
                updated_at timestamp,
                mrp decimal,
                SAP_product_name text,
                brand text,
                id integer,
                name text,
                slug text,
                offer_price decimal,
                offer_description text,
                display_unit text,
                product_type text,
                PRIMARY KEY (barcode, updated_at)
            )
        """.format(schema=self.schema, insert_table=self.insert_table)
        )

        self.curr.execute("""
                        INSERT INTO {schema}.{insert_table} VALUES (
                                                                    '{utc_time}', 
                                                                    '{crawl_ts}',
                                                                    '{barcode}', 
                                                                    '{updated_at}', 
                                                                    '{mrp}', 
                                                                    '{SAP_product_name}',
                                                                    '{brand}',
                                                                    '{id}',
                                                                    '{name}',
                                                                    '{slug}',                                                                    
                                                                    '{offer_price}',
                                                                    '{offer_description}',
                                                                    '{display_unit}',
                                                                    '{product_type}'
                                                                )
                        ON CONFLICT (barcode, updated_at)
                        DO UPDATE
                        SET 
                            utc_time = excluded.utc_time,
                            crawl_ts = excluded.crawl_ts,
                            mrp = excluded.mrp,
                            SAP_product_name = excluded.SAP_product_name,
                            brand = excluded.brand,
                            id = excluded.id,
                            name = excluded.name,
                            slug = excluded.slug,
                            offer_price = excluded.offer_price,
                            offer_description = excluded.offer_description,
                            display_unit = excluded.display_unit,
                            product_type = excluded.product_type
                        """.format(schema=self.schema, insert_table=self.insert_table, **item)
                          )
        self.client.commit()
        logging.info("Upserted a record to the table '{schema}.{insert_table}'".format(
            schema=self.schema, insert_table=self.insert_table))
        return item
