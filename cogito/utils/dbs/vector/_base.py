from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class VectorDBWrapper(ABC):
    """
    Abstract base class for Vector Database Wrappers.
    """

    @abstractmethod
    def connect(self, **kwargs: Any) -> None:
        """
        Connect to the vector database with the required configuration.
        """
        pass

    @abstractmethod
    def create_collection(
        self, collection_name: str, dimension: int, **kwargs: Any
    ) -> None:
        """
        Create a new collection or namespace in the database.
        """
        pass

    @abstractmethod
    def insert(
        self,
        collection_name: str,
        vectors: List[List[float]],
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """
        Insert vectors with optional metadata into the specified collection.
        """
        pass

    @abstractmethod
    def query(
        self,
        collection_name: str,
        query_vector: List[float],
        top_k: int = 10,
        **kwargs: Any
    ) -> List[Dict[str, Any]]:
        """
        Query the database for the top-k most similar vectors.
        """
        pass

    @abstractmethod
    def delete(self, collection_name: str, ids: List[str]) -> None:
        """
        Delete vectors by their IDs.
        """
        pass

    @abstractmethod
    def list_collections(self) -> List[str]:
        """
        List all available collections or namespaces.
        """
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> None:
        """
        Delete a collection or namespace.
        """
        pass
