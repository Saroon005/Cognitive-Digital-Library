from sentence_transformers import SentenceTransformer


class NLPService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def generate_embedding(self, text: str):
        embedding = self.model.encode(text)
        return embedding.tolist()


nlp_service = NLPService()
