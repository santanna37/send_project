from abc import ABC, abstractmethod


class CryptoHashInterface(ABC):

    @abstractmethod
    def create_hash(self, password: str) -> str: pass

    @abstractmethod
    def check_hash(self, password: str, hash_chec: str) -> bool: pass