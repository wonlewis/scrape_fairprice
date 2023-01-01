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
                product_type text,
                barcode text,
                brand text,
                id integer,
                name text,
                slug text,
                mrp decimal,
                updated_at timestamp,
                offer_price decimal,
                offer_description text,
                display_unit text,
                SAP_product_name text,
                PRIMARY KEY (barcode, updated_at)
            )
        """.format(schema=self.schema, insert_table=self.insert_table)
        )

        self.curr.execute("""
                        INSERT INTO {schema}.{insert_table} VALUES (
                                                                    '{utc_time}', 
                                                                    '{product_type}',
                                                                    '{barcode}', 
                                                                    '{brand}', 
                                                                    '{id}', 
                                                                    '{name}', 
                                                                    '{slug}', 
                                                                    '{mrp}', 
                                                                    '{updated_at}', 
                                                                    '{offer_price}', 
                                                                    '{offer_description}',
                                                                    '{display_unit}',
                                                                    '{SAP_product_name}'
                                                                )
                        ON CONFLICT (barcode, updated_at)
                        DO UPDATE
                        SET 
                            utc_time = excluded.utc_time,
                            crawl_ts = excluded.crawl_ts
                            product_type = excluded.product_type
                            brand = excluded.brand
                            id = excluded.id
                            name = excluded.name
                            slug = excluded.slug
                            mrp = excluded.mrp
                            offer_price = excluded.offer_price
                            offer_description = excluded.offer_description
                            display_unit = excluded.display_unit
                            SAP_product_name = excluded.SAP_product_name
                        """.format(schema=self.schema, insert_table=self.insert_table, **item)
                          )
        self.client.commit()
        logging.info("Upserted a record to the table '{schema}.{insert_table}'".format(
            schema=self.schema, insert_table=self.insert_table))
        return item
