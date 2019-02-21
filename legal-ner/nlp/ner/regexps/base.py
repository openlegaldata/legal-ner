from abc import abstractmethod, ABC
from typing import Pattern


class Regexp(ABC):

    @abstractmethod
    def regexp_obj(self) -> Pattern:
        pass

    def normalize(self, groups: dict, full_match: str) -> any:
        return full_match
