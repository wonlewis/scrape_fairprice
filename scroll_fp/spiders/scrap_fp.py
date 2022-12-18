import scrapy
from varname import nameof

drinks = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=drinks&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=drinks&sorting=POPULARITY&storeId=165&url=drinks'
vegetables = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=fruits-vegetables&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=fruits-vegetables&sorting=POPULARITY&storeId=17&url=fruits-vegetables'
dairy = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=dairy-chilled-eggs&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=dairy-chilled-eggs&sorting=POPULARITY&storeId=17&url=dairy-chilled-eggs'
bakery = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=bakery&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=bakery&storeId=17&url=bakery'
meat = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=meat-seafood&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=meat-seafood&sorting=POPULARITY&storeId=17&url=meat-seafood'
staples = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=rice-noodles-cooking-ingredients&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=rice-noodles-cooking-ingredients&sorting=POPULARITY&storeId=17&url=rice-noodles-cooking-ingredients'
household = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=household&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page=2&pageType=category&slug=household&sorting=POPULARITY&storeId=17&url=household'


class QuotesSpider(scrapy.Spider):
    name = "scrap_fp"
    start_urls = [drinks.format(1)]

    def parse(self, response):
        #read json object
        my_data = response.json()

        for product in my_data["data"]["product"]:
            if 'offers' in product:
                offer_price = product["offers"][0]["price"]
                offer_description = product["offers"][0]["description"]
            else:
                offer_price = None
                offer_description = None
            print(dir())
            yield {
                'barcode': product["barcodes"][0],
                'brand': product["brand"]["name"],
                'id': product["brand"]["id"],
                'name': product["name"],
                'slug': product["slug"],
                'images': product["images"],
                'mrp': product["storeSpecificData"][0]["mrp"],
                'updated_at': product["storeSpecificData"][0]["updatedAt"],
                'offer_price': offer_price,
                'offer_description': offer_description,
                'display_unit': product["metaData"]["DisplayUnit"],
                "SAP_product_name": product["metaData"]["SAP Product Name"],
                'product_type': 'drinks'
            }
        curr_page = my_data["data"]["pagination"]["page"]
        total_page = my_data["data"]["pagination"]["total_pages"]
        if my_data["data"]["pagination"]["page"] < 2:
            next_page_url = drinks.format(curr_page+1)
            yield scrapy.Request(next_page_url)
        else:
            next_page_url = drinks.format(1)
            yield scrapy.Request(next_page_url, callback = self.parseVeg)

    def parseVeg(self, response):
        #read json object
        my_data = response.json()

        for product in my_data["data"]["product"]:
            if 'offers' in product:
                offer_price = product["offers"][0]["price"]
                offer_description = product["offers"][0]["description"]
            else:
                offer_price = None
                offer_description = None
            print(dir())
            yield {
                'barcode': product["barcodes"][0],
                'brand': product["brand"]["name"],
                'id': product["brand"]["id"],
                'name': product["name"],
                'slug': product["slug"],
                'images': product["images"],
                'mrp': product["storeSpecificData"][0]["mrp"],
                'updated_at': product["storeSpecificData"][0]["updatedAt"],
                'offer_price': offer_price,
                'offer_description': offer_description,
                'display_unit': product["metaData"]["DisplayUnit"],
                "SAP_product_name": product["metaData"]["SAP Product Name"],
                'product_type': 'drinks'
            }
        curr_page = my_data["data"]["pagination"]["page"]
        total_page = my_data["data"]["pagination"]["total_pages"]
        if my_data["data"]["pagination"]["page"] < 2:
            next_page_url = vegetables.format(curr_page+1)
            yield scrapy.Request(next_page_url, callback=self.parseVeg)
        else:
            next_page_url = dairy.format(1)
            yield scrapy.Request(next_page_url, callback=self.parseDairy)

    def parseDairy(self, response):
        #read json object
        my_data = response.json()

        for product in my_data["data"]["product"]:
            if 'offers' in product:
                offer_price = product["offers"][0]["price"]
                offer_description = product["offers"][0]["description"]
            else:
                offer_price = None
                offer_description = None
            print(dir())
            yield {
                'barcode': product["barcodes"][0],
                'brand': product["brand"]["name"],
                'id': product["brand"]["id"],
                'name': product["name"],
                'slug': product["slug"],
                'images': product["images"],
                'mrp': product["storeSpecificData"][0]["mrp"],
                'updated_at': product["storeSpecificData"][0]["updatedAt"],
                'offer_price': offer_price,
                'offer_description': offer_description,
                'display_unit': product["metaData"]["DisplayUnit"],
                "SAP_product_name": product["metaData"]["SAP Product Name"],
                'product_type': 'drinks'
            }
        curr_page = my_data["data"]["pagination"]["page"]
        total_page = my_data["data"]["pagination"]["total_pages"]
        if my_data["data"]["pagination"]["page"] < 2:
            next_page_url = dairy.format(curr_page+1)
            yield scrapy.Request(next_page_url, callback=self.parseDairy)
        else:
            next_page_url = bakery.format(1)
            yield scrapy.Request(next_page_url, callback=self.parseBakery)

    def parseBakery(self, response):
        #read json object
        my_data = response.json()

        for product in my_data["data"]["product"]:
            if 'offers' in product:
                offer_price = product["offers"][0]["price"]
                offer_description = product["offers"][0]["description"]
            else:
                offer_price = None
                offer_description = None
            print(dir())
            yield {
                'barcode': product["barcodes"][0],
                'brand': product["brand"]["name"],
                'id': product["brand"]["id"],
                'name': product["name"],
                'slug': product["slug"],
                'images': product["images"],
                'mrp': product["storeSpecificData"][0]["mrp"],
                'updated_at': product["storeSpecificData"][0]["updatedAt"],
                'offer_price': offer_price,
                'offer_description': offer_description,
                'display_unit': product["metaData"]["DisplayUnit"],
                "SAP_product_name": product["metaData"]["SAP Product Name"],
                'product_type': 'drinks'
            }
        curr_page = my_data["data"]["pagination"]["page"]
        total_page = my_data["data"]["pagination"]["total_pages"]
        if my_data["data"]["pagination"]["page"] < 2:
            next_page_url = bakery.format(curr_page+1)
            yield scrapy.Request(next_page_url, callback=self.parseBakery)
        else:
            next_page_url = meat.format(1)
            yield scrapy.Request(next_page_url, callback=self.parseMeat)

    def parseMeat(self, response):
        #read json object
        my_data = response.json()

        for product in my_data["data"]["product"]:
            if 'offers' in product:
                offer_price = product["offers"][0]["price"]
                offer_description = product["offers"][0]["description"]
            else:
                offer_price = None
                offer_description = None
            print(dir())
            yield {
                'barcode': product["barcodes"][0],
                'brand': product["brand"]["name"],
                'id': product["brand"]["id"],
                'name': product["name"],
                'slug': product["slug"],
                'images': product["images"],
                'mrp': product["storeSpecificData"][0]["mrp"],
                'updated_at': product["storeSpecificData"][0]["updatedAt"],
                'offer_price': offer_price,
                'offer_description': offer_description,
                'display_unit': product["metaData"]["DisplayUnit"],
                "SAP_product_name": product["metaData"]["SAP Product Name"],
                'product_type': 'drinks'
            }
        curr_page = my_data["data"]["pagination"]["page"]
        total_page = my_data["data"]["pagination"]["total_pages"]
        if my_data["data"]["pagination"]["page"] < 2:
            next_page_url = meat.format(curr_page+1)
            yield scrapy.Request(next_page_url, callback=self.parseMeat)
        else:
            next_page_url = staples.format(1)
            yield scrapy.Request(next_page_url, callback=self.parseStaples)

    def parseStaples(self, response):
        #read json object
        my_data = response.json()

        for product in my_data["data"]["product"]:
            if 'offers' in product:
                offer_price = product["offers"][0]["price"]
                offer_description = product["offers"][0]["description"]
            else:
                offer_price = None
                offer_description = None
            print(dir())
            yield {
                'barcode': product["barcodes"][0],
                'brand': product["brand"]["name"],
                'id': product["brand"]["id"],
                'name': product["name"],
                'slug': product["slug"],
                'images': product["images"],
                'mrp': product["storeSpecificData"][0]["mrp"],
                'updated_at': product["storeSpecificData"][0]["updatedAt"],
                'offer_price': offer_price,
                'offer_description': offer_description,
                'display_unit': product["metaData"]["DisplayUnit"],
                "SAP_product_name": product["metaData"]["SAP Product Name"],
                'product_type': 'drinks'
            }
        curr_page = my_data["data"]["pagination"]["page"]
        total_page = my_data["data"]["pagination"]["total_pages"]
        if my_data["data"]["pagination"]["page"] < 2:
            next_page_url = staples.format(curr_page+1)
            yield scrapy.Request(next_page_url, callback=self.parseStaples)
        else:
            next_page_url = household.format(1)
            yield scrapy.Request(next_page_url, callback=self.parseHousehold)

    def parseHousehold(self, response):
        #read json object
        my_data = response.json()

        for product in my_data["data"]["product"]:
            if 'offers' in product:
                offer_price = product["offers"][0]["price"]
                offer_description = product["offers"][0]["description"]
            else:
                offer_price = None
                offer_description = None
            print(dir())
            yield {
                'barcode': product["barcodes"][0],
                'brand': product["brand"]["name"],
                'id': product["brand"]["id"],
                'name': product["name"],
                'slug': product["slug"],
                'images': product["images"],
                'mrp': product["storeSpecificData"][0]["mrp"],
                'updated_at': product["storeSpecificData"][0]["updatedAt"],
                'offer_price': offer_price,
                'offer_description': offer_description,
                'display_unit': product["metaData"]["DisplayUnit"],
                "SAP_product_name": product["metaData"]["SAP Product Name"],
                'product_type': 'drinks'
            }
        curr_page = my_data["data"]["pagination"]["page"]
        total_page = my_data["data"]["pagination"]["total_pages"]
        if my_data["data"]["pagination"]["page"] < 2:
            next_page_url = household.format(curr_page+1)
            yield scrapy.Request(next_page_url, callback=self.parseHousehold)