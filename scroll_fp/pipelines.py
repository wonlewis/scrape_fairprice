# useful for handling different item types with a single interface
import pg8000
import json
import logging
import os


class PostgresPipeline(object):
    # Init
    user = os.environ.get('DB_USER', '')
    password = os.environ.get('DB_PASSWORD', '')
    host = os.environ.get('DB_HOSTNAME', '')
    database = os.environ.get('DB_DATABASE', '')
    port = os.environ.get('DB_PORT', '')
    schema = os.environ.get('DB_SCHEMA', '')
    insert_table = os.environ.get('DB_INSERT_TABLE', '')

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
                                                                    '{SAP_product_name}'
                                                                )
                        ON CONFLICT (barcode, updated_at)
                        DO UPDATE
                        SET 
                            utc_time = excluded.utc_time,
                            crawl_ts = excluded.crawl_ts,
                            mrp = excluded.mrp,
                            SAP_product_name = excluded.SAP_product_name
                        """.format(schema=self.schema, insert_table=self.insert_table, **item)
                          )
        self.client.commit()
        logging.info("Upserted a record to the table '{schema}.{insert_table}'".format(
            schema=self.schema, insert_table=self.insert_table))
        return item
