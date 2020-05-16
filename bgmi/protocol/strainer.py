"""Base for Data source see :ref:`输出下载结果`

"""
from typing import TYPE_CHECKING, List

from bgmi.helper import abstract

if TYPE_CHECKING:
    from bgmi.core import Subscription
    from bgmi.protocol import source


class Base(metaclass=abstract.Meta):
    @abstract.abstractmethod
    def __init__(self) -> None:
        pass

    @abstract.abstractmethod
    def episodes(
        self, sub: "Subscription", episodes: List["source.Episode"]
    ) -> List["source.Episode"]:
        """remove episode you didn't need

        :param sub: Subscription where episodes got
        :param episodes: episode you want to keep
        :returns: episodes
        """
        return []


class EmptyStrainer(Base):
    def __init__(self) -> None:
        pass

    def episodes(
        self, sub: "Subscription", episodes: List["source.Episode"]
    ) -> List["source.Episode"]:
        return episodes
