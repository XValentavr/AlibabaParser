from celery import Celery


class CeleryClient:
    @staticmethod
    def celery_init_app(application) -> Celery:
        """
        init celery client to work with
        """
        celery_app = Celery(application.name)
        celery_app.config_from_object('celery_config')
        celery_app.set_default()
        return celery_app


celery_client = CeleryClient()
