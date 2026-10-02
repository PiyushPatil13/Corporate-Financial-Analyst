import faiss
import numpy as np

class VectorStore:
    def __init__(self,dimension : int = 384):
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []

    def add(self, text : str,embedding : list[float]) -> None:
        vector = np.array([embedding],dtype="float32")
        self.index.add(vector)
        self.texts.append(text)

    def search(self,query_embedding : list[float], top_k : int = 10) -> list[str]:
        vector = np.array([query_embedding],dtype="float32")
        distances, indices = self.index.search(vector,top_k)
        return [self.texts[i] for i in indices[0] if  0 <= i < len(self.texts)]
    