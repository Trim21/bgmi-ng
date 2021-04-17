from typing import TypeVar

from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.sql import expression

from bgmi.core.series import Series as CoreSeries

T = TypeVar("T", bound=DeclarativeMeta)


class ORMMixin:
    __tablename__: str

    def dict(self: T) -> dict:
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


Base: DeclarativeMeta = declarative_base()
metadata = Base.metadata


class Subscription(Base, ORMMixin):
    __tablename__ = "subscription"

    name = Column(String(50), primary_key=True, nullable=False)
    episode = Column(Integer, nullable=False, server_default="0")
    updating = Column(
        Boolean,
        nullable=False,
        index=False,
        server_default=expression.false(),
    )


class Series(Base, ORMMixin):
    __tablename__ = "series"

    id = Column(String(255), primary_key=True)
    name = Column(String(255), index=True, nullable=False)
    source = Column(String(40), primary_key=True, nullable=False, index=True)
    episode = Column(Integer, nullable=False, server_default="0")
    start = Column(Integer, nullable=False, server_default="0")
    sub_name = Column(String(50), index=True, nullable=False, server_default="")

    def to_core_obj(self) -> CoreSeries:
        return CoreSeries(
            id=self.id,
            name=self.name,
            source=self.source,
            latest_episode=self.episode,
            first_episode=self.start,
        )


class Episode(Base, ORMMixin):
    __tablename__ = "episode"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    source = Column(String(40), index=True, nullable=False)
    series = Column(String(255), index=True)
    url = Column(String(255))
    date = Column(Date)


__all__ = [
    "Column",
    "Integer",
    "String",
    "Series",
    "Subscription",
]


if __name__ == "__main__":
    import os.path

    from sqlalchemy import create_engine

    print(os.path.expanduser("~/.bgmi/app.db"))
    engine = create_engine("sqlite:///" + os.path.expanduser("~/.bgmi/app.db"))
    Base.metadata.create_all(engine)
