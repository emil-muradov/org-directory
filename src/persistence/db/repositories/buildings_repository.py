from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from schema import Building


class BuildingsRepository(ABC):
    @abstractmethod
    def find_building_by_id(self, building_id: int) -> Building:
        pass

