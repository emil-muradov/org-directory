from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from schema import Industry


class IndustriesRepository(ABC):
    @abstractmethod
    def find_industry_by_id(self, industry_id: int) -> Industry:
        pass
