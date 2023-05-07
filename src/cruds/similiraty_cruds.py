from create_engine import session
from models.similarity_model import SimilarityModel


class SimilarityCRUDS:
    """
    Class that works with similarity rate
    """

    default_similarity = 0.9

    def get_similarity(self) -> SimilarityModel:
        """
        Get existing similarity
        :return: similarity from database
        """
        exists = session.query(SimilarityModel).first()

        if not exists:
            self.add_default_similarity()
        return session.query(SimilarityModel).first()

    @classmethod
    def add_default_similarity(cls):
        """
        Add default similarity
        """
        similarity = SimilarityModel(similarity=cls.default_similarity)
        session.add(similarity)
        session.commit()

    @staticmethod
    def change_similarity(new_similarity: float):
        """
        Change existing similarity no new got from API
        :param new_similarity: similarity from API
        :return: None
        """
        old_similarity = session.query(SimilarityModel).first()
        old_similarity.similarity = new_similarity
        session.commit()

    @staticmethod
    def remove_similarity():
        """
        Remove existing similarity from DB
        :return: None
        """
        similarity = session.query(SimilarityModel).first()
        session.delete(similarity)
        session.commit()
