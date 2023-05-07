from uuid import UUID

from celery import shared_task, Task

from services.alibaba.search_by_api import alibaba_search_by_api
from tasks.celery_task_interface import CeleryTaskInterface


class CeleryAlibabaTasks(CeleryTaskInterface):

    @staticmethod
    @shared_task(base=Task, name='create_text_finder_task')
    def create_text_finder_task(amazon_product_id: UUID, text: str):
        """
        Run task to get alibaba info using text
        :return: None
        """
        from handlers.endpoint_handlers.amazon_endpoint_helper import amazon_endpoint_helper

        alibaba_product_ids = alibaba_search_by_api.get_products_by_text(amazon_product_id, text=text)
        if alibaba_product_ids:
            amazon_endpoint_helper.aws_trigger(amazon_product_id, alibaba_ids=alibaba_product_ids)
            return alibaba_product_ids
        return


celery_alibaba_tasks = CeleryAlibabaTasks()
