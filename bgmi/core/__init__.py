"""BGmi core

``app`` manager ``Subscription``

a ``Subscription`` has many ``Series``

``Subscription`` is created by application.

``Series`` is created by source
"""
from bgmi.core import namespace
from bgmi.core.application import BGmi
from bgmi.core.series import Series
from bgmi.core.subscription import Subscription

__all__ = [
    "namespace",
    "BGmi",
    "Series",
    "Subscription",
]
