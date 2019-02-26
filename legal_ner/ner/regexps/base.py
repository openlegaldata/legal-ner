from abc import abstractmethod, ABC
from typing import Pattern


class Regexp(ABC):

    @abstractmethod
    def regexp_obj(self) -> Pattern:
        pass

    @abstractmethod
    def normalize(self, groups: dict, full_match: str) -> any:
        pass
