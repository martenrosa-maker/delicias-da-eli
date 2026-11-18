from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar, Optional

# Declaração do tipo genérico para ser reutilizado por outros modelos (ex: Produto, Mensagem, etc.)
T = TypeVar("T")

class IBaseRepository(ABC, Generic[T]):
    """
    Interface base [REPOSITORY] para garantir padronização em todos os repositórios.
    """
    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass