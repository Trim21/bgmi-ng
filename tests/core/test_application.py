import typing
from typing import Iterable, List, Tuple

import pytest
import stevedore

from bgmi3.core import BGmi, Series, Subscription, namespace
from bgmi3.model import Config
from bgmi3.protocol import backend, source
from bgmi3.protocol.source import Episode, Subtitle


class MockBackend(backend.Base):
    version = "233"

    def __init__(self):
        self.subscriptions = []

    @classmethod
    def install(cls, **kwargs) -> None:
        pass

    def get_series(self, source_id: str, name: str) -> Series:
        pass

    def add_subscription(self, sub: Subscription) -> None:
        self.subscriptions.append(sub)

    def save_subscription(self, sub: Subscription) -> None:
        pass

    def remove_subscription(self, sub: Subscription) -> None:
        pass

    def get_subscription(self, sub_name: str) -> Subscription:
        pass

    def get_all_subscription(
        self, filters: typing.Dict[str, typing.Any] = None
    ) -> List[Subscription]:
        return self.subscriptions


class MockSource(source.Base):
    name = "mock source"
    id = "mock-source"

    def fetch_series_and_subtitle_group(self) -> Tuple[List[Series], List[Subtitle]]:
        pass

    def fetch_episode_of_series(
        self, series_id: str, max_page: int, subtitle_list: List[str] = None
    ) -> Iterable[Episode]:
        pass

    def search_by_keyword(
        self, keyword: str, max_page: int = None
    ) -> Iterable[Episode]:
        pass


@pytest.fixture()
def mock_backend():
    return MockBackend()


def test_create(mock_backend):
    app = BGmi(config=Config(), backend=mock_backend)
    app.create("hello")
    assert len(mock_backend.subscriptions) == 1
    assert mock_backend.subscriptions[0].name == "hello"


def test_add(mock_backend):
    sub = Subscription(name="233")
    mock_backend.subscriptions.append(sub)
    app = BGmi(config=Config(), backend=mock_backend)
    app.source_mgr = {"source": ""}
    app.add(sub.name, "source", "name")


def test_fetch_episode(mock_backend):
    class MockSeries(Series):
        pass

        @property
        def driver(self) -> "source.Base":
            return stevedore.DriverManager(
                namespace.SOURCE, self.source, invoke_on_load=True
            ).driver

    app = BGmi(config=Config(), backend=mock_backend)
    app.subscriptions = []
