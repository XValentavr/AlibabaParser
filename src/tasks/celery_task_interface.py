from abc import ABC, abstractmethod


class CeleryTaskInterface(ABC):
    """
    Class to create interface for celery tasks
    """

    @abstractmethod
    def create_text_finder_task(self):
        raise NotImplementedError("Implement me!")
