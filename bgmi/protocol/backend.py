"""Abstract Base Classes for Backend"""
import abc
import typing

import bgmi.exc
from bgmi.helper import abstract

if typing.TYPE_CHECKING:
    import bgmi.core


class Base(metaclass=abstract.Meta):
    """base class for backend"""

    #: class attribute for attribute version
    version: str = abstract.abstract_class_attribute()

    @classmethod
    @abc.abstractmethod
    def install(cls, config: dict) -> None:
        """install backend, like create tables,
         only will be called after ``Backend`` change

         :param config: backend config
         """

    # @classmethod
    # @abc.abstractmethod
    # def backend_upgrade(cls, old_version: str, new_version: str) -> None:
    #     """upgrade from old version,
    #     will be called after ``BGmi`` find plugin version changes
    #
    #     :param old_version: old installed version
    #     :param new_version: new installed version
    #     """

    @abc.abstractmethod
    def add_subscription(self, sub: "bgmi.core.Subscription") -> None:
        """save a subscription to backend

        ..
            # noqa: DAR202

        :param sub: subscription name
        """

    @abc.abstractmethod
    def remove_subscription(self, sub: "bgmi.core.Subscription") -> None:
        """remove a subscription from backend

        do nothing when record doesn't exist

        ..
            # noqa: DAR202

        :param sub: subscription name
        """

    @abc.abstractmethod
    def get_subscription(self, sub_name: str) -> "bgmi.core.Subscription":
        """get a subscription from backend

        ..
            # noqa: DAR202

        :param sub_name: subscription name
        :return: Subscription matched
        :raises bgmi.exc.SubscriptionNotFollowed: Subscription not found
        """

    @abc.abstractmethod
    def save_subscription(self, sub: "bgmi.core.Subscription") -> None:
        """save or create subscription and it's series to backend

        if subscription is not dirty, do nothing

        :param sub: subscription to save
        """

    @abc.abstractmethod
    def get_all_subscription(
        self, filters: typing.Dict[str, typing.Any] = None
    ) -> typing.List["bgmi.core.Subscription"]:
        """get a subscription from backend

        ..
            # noqa: DAR202

        :param filters: filter when getting all subscription
        :return: Subscription matched
        :raises bgmi.exc.SubscriptionNotFollowed: Subscription not found
        """

    @abc.abstractmethod
    def get_series(self, source_id: str, name: str) -> "bgmi.core.Series":
        """get a series from backend

        ..
            # noqa: DAR202

        :param source_id: source id
        :param name: series name
        :return: Series matched
        :raises bgmi.exc.SeriesNotFollowed: Series not found
        """
