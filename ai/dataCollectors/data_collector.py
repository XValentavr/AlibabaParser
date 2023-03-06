from collections import OrderedDict

from ai.dataCollectors.base_data_collector import BaseDataCollector


class DataCollector(BaseDataCollector):
    def __init__(self, amazon: OrderedDict, alibaba: OrderedDict):
        self.amazon = amazon
        self.alibaba = alibaba

    def get_amazon_products(self) -> dict:
        return self.amazon

    def get_alibaba_product(self) -> dict:
        return self.alibaba

    def extract_product_info(self, product: OrderedDict, key: str = 'link') -> dict or str:
        data = super().extract_product_data(product=product, key=key)
