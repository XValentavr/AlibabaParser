from uuid import UUID

from create_engine import session

from models.average_price import AveragePriceModel


class AverageCRUDS:
    """
    Class to work with average model
    """

    @staticmethod
    def insert_average(amazon_product_id: UUID, average: str):
        """
        insert average price to database
        :param amazon_product_id: amazon product to create average
        :param average: average price of product on alibaba
        :return: None
        """
        average = AveragePriceModel(
            average=average,
            amazon_product_id=amazon_product_id)
        session.add(average)
        session.commit()

    @staticmethod
    def get_average_price(amazon_product_id: UUID):
        """
        Get average price from the database
        :param amazon_product_id: amazon product id to get info about
        :return: None
        """
        return (
            session.query(AveragePriceModel)
            .filter(AveragePriceModel.amazon_product_id == amazon_product_id)
            .first()
        )


average_cruds = AverageCRUDS()
