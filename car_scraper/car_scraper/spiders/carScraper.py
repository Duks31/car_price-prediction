import scrapy
from car_scraper.items import CarScraperItem

class CarscraperSpider(scrapy.Spider):
    name = "carScraper"
    allowed_domains = ["www.cars45.com"]
    start_urls = ["https://www.cars45.com/listing"]

    def parse(self, response):
        cars = response.css("section.cars-grid.grid a.car-feature--wide-mobile")
        for car in cars:
            car_url = car.css("::attr(href)").get()
            yield response.follow(car_url, callback=self.parse_car_page)

        # next page
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback = self.parse)

    def parse_car_page(self, response): 
        general_info = response.xpath('//div[@class="general-info grid"]/div')
        tags = response.css("div.main-details__tags span::text").getall()
        svg_info = response.css("div.svg.flex > div")
    
        car_item = CarScraperItem()
        car_item["car_id"] = response.url.split("/")[-1]
        car_item["city"] = response.css("p.main-details__region::text").get()
        car_item["price"] = response.css("h5.main-details__name__price::text").get()
        car_item["condition"] = tags[0] if len(tags) > 0 else None
        car_item["transmission"] = tags[1] if len(tags) > 1 else None
        car_item["mileage"] = tags[2] if len(tags) > 2 else None
        for svg in svg_info:
            alt_text = svg.css("img::attr(alt)").get()
            value = svg.css("span.tab-content__svg__title::text").get()
            if alt_text == "Body":
                car_item["body_type"] = value
            elif alt_text == "Fuel":
                car_item["fuel_type"] = value
            elif alt_text == "Transmission":
                car_item["transmission"] = value

        for info in general_info:
            name = info.xpath('.//span[@class="general-info__value"]/text()').get()
            value = info.xpath('.//p[@class="general-info__name"]/text()').get()
            if name and value:
                name = name.strip()
                value = value.strip()
                if name == "Make":
                    car_item["make"] = value
                elif name == "Model":
                    car_item["model"] = value
                elif name == "Year of manufacture":
                    car_item["year_of_manufacture"] = value
                elif name == "Colour":
                    car_item["color"] = value
                elif name == "Engine Size":
                    car_item["engine_size"] = value
                elif name == "Registered city":
                    car_item["registered_city"] = value
                elif name == "Selling Condition":
                    car_item["selling_condition"] = value
                elif name == "Bought Condition":
                    car_item["bought_condition"] = value

        yield car_item
