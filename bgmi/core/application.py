"""application"""
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

import stevedore
import stevedore.extension

from bgmi.core import namespace
from bgmi.core.series import Series
from bgmi.core.subscription import Subscription
from bgmi.db import table
from bgmi.exc import SeriesNotFollowed, SubscriptionNotFollowed
from bgmi.model import Config
from bgmi.protocol import backend, output, source


@dataclass
class BGmi:
    """BGmi Core

    example:

    .. code-block:: python

        bgmi = BGmi(config=Config())
        subscription_name = "超炮"
        bgmi.create(subscription_name)
        bgmi.add(sub_name=subscription_name, source="mikan", name="科学的超电磁炮T")
        bgmi.remove(subscription_name, "mikan")
        bgmi.delete(subscription_name)

    """

    config: Config
    backend: backend.Base
    logger: logging.Logger = logging.getLogger("BGmi")
    source_mgr: List[source.Base] = field(default_factory=lambda: BGmi.load_source())
    output_mgr: List[output.Base] = field(default_factory=lambda: BGmi.load_output())
    subscriptions: List[Subscription] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.subscriptions = self.backend.get_all_subscription({"updating": True})

    def create(self, name: str) -> Subscription:
        """create a subscription

        if a subscription with same name has existed, return existed subscription

        :param name: subscription name
        :return: Subscription just created
        """
        for subscription in self.subscriptions:
            if subscription.name == name:
                return subscription
        subscription = Subscription(name)
        self.backend.add_subscription(subscription)
        return subscription

    def delete(self, name: str) -> None:
        """delete subscription

        :param name: subscription name
        """
        self.backend.remove_subscription(Subscription(name))

    def add(self, sub_name: str, source_name: str, name: str) -> Series:
        """add series to subscription

        ..
            # noqa: DAR401

        :param sub_name: subscription name
        :param source_name: which source from
        :param name: name in source
        :return: series just added
        :raises SubscriptionNotFollowed: Subscription not found
        :raises SeriesNotFollowed: Series not found in this source
        """

        try:
            # subscription = self.backend.getSubscription(sub_name)
            series = self.backend.get_series(source_name, name)
        except SeriesNotFollowed as e:
            self.logger.warning(
                "series %s doesn't have series %s", sub_name, source_name
            )
            raise e from None

        for subscription in self.subscriptions:
            if subscription.name == sub_name:
                subscription.add(series)
                self.backend.save_subscription(subscription)
                return series

        self.logger.warning("subscription %s not found", sub_name)
        raise SubscriptionNotFollowed()

    def remove(self, sub_name: str, source_name: str) -> None:
        """remove series from subscription

        :param sub_name: subscription name
        :param source_name: source id
        """

    @classmethod
    def load_source(cls) -> List[source.Base]:
        """load add source from entry_points

        :return: return a list contains enabled sources
        """
        return [
            x.plugin
            for x in stevedore.ExtensionManager(
                namespace.SOURCE, invoke_on_load=True
            ).extensions
        ]

    @classmethod
    def load_output(cls) -> List[output.Base]:
        return [
            x.plugin
            for x in stevedore.ExtensionManager(
                namespace.OUTPUT, invoke_on_load=True
            ).extensions
        ]

    def execute(self) -> None:
        for subscription in self.subscriptions:
            episodes = self.fetch_episodes(subscription)
            if episodes:
                for ext in self.output_mgr:
                    ext.execute(
                        subscription, episodes[0].url, save_path=self.config.save_path
                    )

    def fetch_episodes(self, subscription: Subscription) -> List[source.Episode]:
        episodes: List[source.Episode] = []
        for ser in subscription.series:
            try:
                for episode in ser.driver.fetch_episode_of_series(ser.id):
                    episodes.append(
                        table.Episode(
                            title=episode.title,
                            url=episode.url,
                            source=ser.source,
                            series=ser.id,
                            date=episode.time or datetime.fromtimestamp(0),
                        )
                    )
            except stevedore.extension.NoMatches:
                pass

        episodes.sort(key=lambda x: x.episode)
        for s in subscription.strainers:
            episodes = s.episodes(subscription, episodes)
        return episodes
