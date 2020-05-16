import os
import os.path

import requests

import bgmi.exc
from bgmi.core import Subscription
from bgmi.protocol import output


class MyOutput(output.Base):
    @classmethod
    def require(cls) -> None:  # pragma: no cover
        pass

    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def execute(
        self, subscription: "Subscription", torrent: str, save_path: str
    ) -> None:  # pragma: no cover
        if not torrent.startswith("http"):
            return
        try:
            r = requests.get(torrent)
        except requests.ConnectionError as e:
            raise bgmi.exc.ConnectError from e
        filename = os.path.basename(torrent)
        with open(os.path.join(save_path, filename), "wb") as f:
            f.write(r.content)
