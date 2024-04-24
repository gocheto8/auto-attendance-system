from typing import Literal

from annoy import AnnoyIndex


class Recognizer:
    def __init__(
        self,
        annoy_tree_file: str,
        vector_size: int,
        distance_metric: Literal["angular", "euclidean", "manhattan", "hamming", "dot"],
    ) -> None:
        self.vector_size = vector_size
        self.stored_embedding_tree = AnnoyIndex(vector_size, distance_metric)
        self.stored_embedding_tree.load(annoy_tree_file)
        pass

    def recognize(self, vector: list) -> int:
        if len(vector) != self.vector_size:
            raise ValueError
        index = self.stored_embedding_tree.get_nns_by_vector(
            vector, 1, search_k=-1, include_distances=True
        )
        return index
