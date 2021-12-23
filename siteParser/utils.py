import json

from siteParser.items import ProductItem


class ProductUtils:
    def obj_to_json(self, product):
        json.dumps(product.__dict__)

    def json_to_obj(self, product_json):
        j = json.loads(product_json)
        ProductItem(**j)
