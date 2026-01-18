from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from schema import Phone


class PhonesRepository(ABC):
    @abstractmethod
    def find_organization_phones(self, organization_id: int) -> list[Phone]:
        pass
