from typing import List

from pydantic import BaseModel

from bgmi.model.bangumi_base import UpdateTime
from bgmi.model.status import SeriesStatus


class Series(BaseModel):
    id: int
    name: str
    cover: str
    status: SeriesStatus = SeriesStatus.UPDATING
    update_time: UpdateTime
    subtitle_group: List[str]
    source_id: str
