from create_engine import session
from models.similarity_model import SimilarityModel


class SimilarityCRUDS:
    default_similarity = 0.9

    def get_similarity(self):
        exists = session.query(SimilarityModel).first()

        if not exists:
            self.add_default_similarity()
        return session.query(SimilarityModel).first().similarity

    @classmethod
    def add_default_similarity(cls):
        similarity = SimilarityModel(similarity=cls.default_similarity)
        session.add(similarity)
        session.commit()

    @staticmethod
    def change_similarity(new_similarity: float):
        old_similarity = session.query(SimilarityModel).first()
        old_similarity.similarity = new_similarity
        session.commit()

    @staticmethod
    def remove_similarity():
        similarity = session.query(SimilarityModel).first()
        session.delete(similarity)
        session.commit()
