import scrapy

drinks = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=drinks&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=drinks&sorting=POPULARITY&storeId=165&url=drinks'

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
            yield {
                'barcode': product["barcodes"][0],
                'brand': product["brand"]["name"],
                'id': product["brand"]["id"],
                'name': product["name"],
                'slug': product["slug"],
                'images': product["images"],
                'mrp': product["storeSpecificData"][0]["mrp"],
                'offer_price': offer_price,
                'offer_description': offer_description,
                'display_unit': product["metaData"]["DisplayUnit"],
                "SAP_product_name": product["metaData"]["SAP Product Name"]
            }
        curr_page = my_data["data"]["pagination"]["page"]
        total_page = my_data["data"]["pagination"]["total_pages"]
        if my_data["data"]["pagination"]["page"] < total_page:
            next_page_url = drinks.format(curr_page+1)
            yield scrapy.Request(next_page_url)
