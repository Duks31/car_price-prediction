# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CarScraperPipeline:
    def process_item(self, item, spider):
        
        # removing the Naira sign from price
        if "price" in item:
            item["price"] = int(item["price"].replace("₦", "").replace(",", "").strip())

        # removing "km" from mileage
        if "mileage" in item:
            item["mileage"] = int(item["mileage"].split(" ")[0])

        # spliting city to get the particular city
        if "city" in item:
            item["city"] = item["city"].split(",")[-1].strip()

        # converting engine size to int
        if "engine_size" in item:
            item["engine_size"] = int(item["engine_size"])

        return item


class PostgresNoDuplicatesPipeline:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = psycopg2.connect(
            host="localhost",
            database="car_data",
            user="postgres",
            password="Jan312018.",
        )
        self.cur = self.connection.cursor()

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cars (
                id serial PRIMARY KEY,
                car_id VARCHAR(50) UNIQUE,
                make VARCHAR(50),
                model VARCHAR(50),
                year_of_manufacture TEXT,
                color TEXT,
                condition TEXT,
                mileage INT,
                engine_size INT,
                registered_city TEXT,
                selling_condition TEXT,
                bought_condition TEXT,
                city TEXT,
                price INT,
                body_type TEXT,
                fuel_type TEXT,
                transmission TEXT
                            )
            """
        )
        self.connection.commit()

    def process_item(self, item, spider):
        try:
            self.store_db(item, spider)
        except psycopg2.Error as e:
            spider.logger.error(f"Error inserting data into database: {e}")
        return item

    def store_db(self, item, spider):
        try:
            car_id = item.get("car_id")
            assert isinstance(car_id, str), f"car_id is not a string: {car_id}"

            self.cur.execute(
                """ 
            INSERT INTO cars (car_id, make, model, year_of_manufacture, color, condition,
                                  mileage, engine_size, registered_city, selling_condition, 
                                  bought_condition, city, price, body_type, fuel_type, transmission)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (car_id) DO NOTHING
                """,
                (
                    str(item.get("car_id")),
                    item.get("make"),
                    item.get("model"),
                    item.get("year_of_manufacture"),
                    item.get("color"),
                    item.get("condition"),
                    item.get("mileage"),
                    item.get("engine_size"),
                    item.get("registered_city"),
                    item.get("selling_condition"),
                    item.get("bought_condition"),
                    item.get("city"),
                    item.get("price"),
                    item.get("body_type"),
                    item.get("fuel_type"),
                    item.get("transmission"),
                ),
            )
            self.connection.commit()
            return item
        except psycopg2.Error as e:
            self.connection.rollback()
            spider.logger.error(f"Error inserting data into database: {e}")

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
