# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarScraperItem(scrapy.Item):
    car_id = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    year_of_manufacture = scrapy.Field()
    color = scrapy.Field()
    condition = scrapy.Field()
    mileage = scrapy.Field()
    engine_size = scrapy.Field()
    registered_city = scrapy.Field()
    selling_condition = scrapy.Field()
    bought_condition = scrapy.Field()
    city = scrapy.Field()
    price = scrapy.Field()
    body_type = scrapy.Field()
    fuel_type = scrapy.Field()
    transmission = scrapy.Field()