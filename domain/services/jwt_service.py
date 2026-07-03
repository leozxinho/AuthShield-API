from abc import ABC, abstractmethod

class JWTService(ABC):
    @abstractmethod
    def encode_token(self, payload: dict) -> str:
        """"Codifica um payload em um token JWT."""
        ...

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """"Decodifica um token JWT em um payload."""
        ...