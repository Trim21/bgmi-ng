"""BGmi core

``app`` manager ``Subscription``

a ``Subscription`` has many ``Series``

``Subscription`` is created by application.

``Series`` is created by source
"""
from bgmi3.core import namespace
from bgmi3.core.application import BGmi
from bgmi3.core.series import Series
from bgmi3.core.subscription import Subscription

__all__ = [
    "namespace",
    "BGmi",
    "Series",
    "Subscription",
]
