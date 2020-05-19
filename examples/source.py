from typing import List, Tuple

import bgmi.protocol.source
from bgmi.protocol import source


class MySource(source.Base):
    name = "my source"
    id = "my-source"

    def fetch_series_and_subtitle_group(
        self,
    ) -> Tuple[List[source.Series], List[source.Subtitle]]:
        return (
            [
                bgmi.protocol.source.Series.parse_obj(
                    {
                        "id": "1",
                        "status": 0,
                        "update_time": "mon",
                        "subtitle_group": ["1", "2"],
                        "name": "ID:INVADED",
                    }
                ),
                bgmi.protocol.source.Series.parse_obj(
                    {
                        "id": "2",
                        "update_time": "Fri",
                        "subtitle_group": ["1"],
                        "name": "科学的超电磁炮T",
                    }
                ),
            ],
            [
                source.Subtitle(id="1", name="subtitle group 1"),
                source.Subtitle(id="2", name="subtitle group 2"),
            ],
        )

    def fetch_episode_of_series(
        self, series_id: str, subtitle_list: List[str] = None
    ) -> List[source.Episode]:
        return [
            source.Episode.parse_obj(
                {
                    "title": "title",
                    "download": "magnet:?xt=urn:btih:233",
                    "episode": 1,
                    "time": 1582200671,
                    "subtitle_group": "1",
                }
            ),
            source.Episode.parse_obj(
                {
                    "title": "title",
                    "download": "https://example.com/a.torrent",
                    "episode": 2,
                    "time": "2019-12-15",
                }
            ),
        ]

    def search_by_keyword(
        self, keyword: str, max_page: int = None
    ) -> List[source.Episode]:
        return [
            source.Episode.parse_obj(
                {
                    "title": "title",
                    "download": "https://example.com/a.torrent",
                    "episode": 2,
                    "time": "2019-12-15",
                }
            ),
        ]
