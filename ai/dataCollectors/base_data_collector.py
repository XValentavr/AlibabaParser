from collections import OrderedDict


class BaseDataCollector:

    @staticmethod
    def extract_product_data(product: OrderedDict, key: str = 'link') -> str or dict:
        return product.get(key)
