"""Base for Data source see :ref:`输出下载结果`

"""
from typing import TYPE_CHECKING

from bgmi.helper import abstract

if TYPE_CHECKING:
    from bgmi.core import Subscription


class Base(metaclass=abstract.Meta):
    """Base class for all output plugin like notify and downloader delegate"""

    @abstract.abstractmethod
    def __init__(self, config: dict) -> None:
        """init

        :param config: config dict user defined in config file.
        """

    @classmethod
    @abstract.abstractmethod
    def require(cls) -> None:
        """
        Implement this classmethod if your download delegate has some additional requires

        .. warning::

            You should not install python package here,
            because it may break other packages.

        :raises RequireNotSatisfiedError:
            If some requirements not satisfied. like missing bin or python package.
            Don't raise ``ImportError``, catch it and describe it in message.

        """

    @abstract.abstractmethod
    def execute(
        self, subscription: "Subscription", torrent: str, save_path: str
    ) -> None:
        """plugin do its works

        :param subscription: subscription
        :param torrent: http(s) or magnet url of torrent file
        :param save_path: video file save path

        :raises ConnectError: Any connection error
        :raises AuthError: If RPC server require authorization
        """
