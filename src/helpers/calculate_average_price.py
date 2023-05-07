from typing import List

from cruds.average_cruds import average_cruds
from models.most_similar_model import MostSimilarModel


class CalculateAveragePrice:
    """
    Class to calculate average price
    """

    @staticmethod
    def calculator(similar: List[MostSimilarModel]):
        """
        Method to calculate average price
        :param similar: similar product to get price of
        :return: average price of similar products
        """
        average = sum([float(sim.alibaba_source.min_price)
                       for sim in similar if sim.alibaba_source.min_price]) / len(similar) - 1

        average_cruds.insert_average(average=average, amazon_product_id=similar[0].amazon_source_id)
        return average


calculate_average_price = CalculateAveragePrice()
