from create_engine import session
from src.models.similarity_model import SimilarityModel


class SimilarityCRUDS:

    @staticmethod
    def add_default_similarity():
        similarity = SimilarityModel(similarity=0.9)
        session.add(similarity)
        session.commit()

    def get_similarity(self):
        exists = session.query(SimilarityModel).first()
        print(exists)
        if not exists:
            self.add_default_similarity()
        return session.query(SimilarityModel).first().similarity

    @staticmethod
    def change_similarity(new_similarity: float):
        old_similarity = session.query(SimilarityModel).first()
        old_similarity.similarity = new_similarity
        session.commit()

    @staticmethod
    def remove_similarity():
        try:
            similarity = session.query(SimilarityModel).first()
            session.delete(similarity)
            session.commit()
            return True
        except Exception:
            return False


sim = SimilarityCRUDS()
print(sim.get_similarity())
