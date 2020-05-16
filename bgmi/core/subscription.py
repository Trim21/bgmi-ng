import dataclasses
from typing import List

from bgmi.core.series import Series
from bgmi.exc import SubscriptionNotFollowed
from bgmi.protocol import strainer


@dataclasses.dataclass
class Subscription:
    name: str
    updating: bool = True
    episode: int = 1
    series: List[Series] = dataclasses.field(default_factory=list)
    _dirty: bool = False
    strainers: List[strainer.Base] = dataclasses.field(
        default_factory=lambda: [strainer.EmptyStrainer()]
    )

    def add(self, series: Series) -> Series:
        self.series.append(series)
        self._dirty = True
        return series

    def remove(self, source: str) -> None:
        for s in self.series:
            if s.name == source:
                self.series.remove(s)
                self._dirty = True
                return

        raise SubscriptionNotFollowed()

    @property
    def dirty(self) -> bool:
        return self._dirty
