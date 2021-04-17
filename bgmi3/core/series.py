import dataclasses
import typing

import stevedore

from bgmi3.core import namespace

if typing.TYPE_CHECKING:
    from bgmi3 import protocol


@dataclasses.dataclass
class Series:
    id: str
    name: str
    source: str
    first_episode: int = 1
    latest_episode: int = 1

    @property
    def driver(self) -> "protocol.source.Base":
        return typing.cast(
            protocol.source.Base,
            stevedore.DriverManager(
                namespace.SOURCE, self.source, invoke_on_load=True
            ).driver,
        )

    @property
    def episode(self) -> int:
        return self.latest_episode - self.first_episode + 1
