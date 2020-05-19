"""Base for Data source see :ref:`添加数据源`"""
from datetime import datetime
from typing import Iterable, List, Optional, Tuple

from pydantic import AnyHttpUrl, BaseModel

from bgmi import model
from bgmi.helper import abstract


class Series(BaseModel):
    id: str
    name: str
    status: model.SeriesStatus = model.SeriesStatus.UPDATING
    update_time: model.UpdateTime
    subtitle_group: List[str]  #: list of subtitle group id
    cover: Optional[AnyHttpUrl]


class Subtitle(BaseModel):
    id: str
    name: str


class Episode(BaseModel):
    url: str
    title: str
    episode: int
    time: Optional[datetime]
    subtitle_group: Optional[str]


class Base(metaclass=abstract.Meta):
    """Base class for all data source"""

    name = abstract.abstract_class_attribute()
    """user readable source name, should be defined as class attribute"""

    id = abstract.abstract_class_attribute()
    """source id, should be defined as class attribute"""

    @abstract.abstractmethod
    def fetch_series_and_subtitle_group(
        self,
    ) -> Tuple[List[Series], List[Subtitle]]:  # pragma: no cover
        """return a list of all bangumi and a list of all subtitle group

        list of bangumi dict:
        update time should be one of
        ``['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']``
        (:py:class:`bgmi.model.UpdateTime`)

        .. warning::

            cover should start with ``http://`` or ``https://``

        .. code-block:: python

            [
                ...,
                bgmi.protocol.source.Series(
                    **{
                        "id": "1234",
                        "status": model.SeriesStatus.UPDATING,
                        "subtitle_group": ["123", "456"],  # list of id of subtitle group
                        "name": "名侦探柯南",
                        "update_time": "mon",
                        "cover": "https://www.example.com/data/images/cover1.jpg",
                    }
                ),
                ...,
            ]

        list of subtitle group dict:

        .. code-block:: python

            [
                ...,
                bgmi.protocol.source.Subtitle(id="233", name="bgmi字幕组"),
                ...,
            ]


        :return: list of series, list of subtitile group
        :rtype: (list[dict], list[dict])
        """
        return [], []

    @abstract.abstractmethod
    def fetch_episode_of_series(
        self, series_id: str, subtitle_list: List[str] = None
    ) -> Iterable[Episode]:  # pragma: no cover
        """get all episode by series id

        :param series_id: series_id
        :param subtitle_list: list of subtitle group
        :type subtitle_list: list
        :return: list of episode
        """
        return []

    @abstract.abstractmethod
    def search_by_keyword(
        self, keyword: str, max_page: int = None
    ) -> Iterable[Episode]:
        """
        search torrent by arguments.
        return a list of dict with at least 4 key: download, name, title, episode.
        Other keys are omitted.

        :param keyword: search key word
        :type keyword: str
        :param max_page: how many page to fetch from website
        :type max_page: int

        :return: list of episode search result
        :rtype: List[dict]
        """
        return []
