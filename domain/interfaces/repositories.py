from abc import ABC, abstractmethod # Classe abstrata para criação de contratos
from domain.entities.users import User # Importa a entidade User

class UsersRepositoryInterface(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        # O método create_user é abstrato e deve ser implementado por qualquer classe que herde de UsersRepositoryInterface
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User: 
        # O método get_user_by_email é abstrato e deve ser implementado por qualquer classe que herde de UsersRepositoryInterface
        pass    