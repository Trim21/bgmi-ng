import os
import sqlite3
import typing

import sqlalchemy as sa
import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import bgmi.core
from bgmi import db
from bgmi.db import table
from bgmi.protocol import backend


class SQLiteBackend(backend.Base):
    version = "init"

    @classmethod
    def create_engine(cls) -> sa.engine.base.Engine:
        return create_engine("sqlite:///" + os.path.expanduser("./tmp/test.db"))

    @classmethod
    def install(cls, config: dict) -> None:
        engine = cls.create_engine()
        db.Base.metadata.create_all(engine)

    def __init__(self) -> None:
        self.Session = sessionmaker(self.create_engine())

    def add_subscription(self, sub: "bgmi.core.Subscription") -> None:

        session = self.Session()
        session.add(
            db.table.Subscription(
                name=sub.name, episode=sub.episode, updating=sub.updating
            )
        )
        try:
            session.commit()
        except sa.exc.IntegrityError as e:
            session.rollback()
            if isinstance(e.orig, sqlite3.IntegrityError):
                session.execute(
                    sa.update(
                        db.table.Subscription,
                        db.table.Subscription.name == sub.name,
                        values={
                            "name": sub.name,
                            "episode": sub.episode,
                            "updating": sub.updating,
                        },
                    )
                )
                session.commit()
            else:
                raise

    def remove_subscription(self, sub: "bgmi.core.Subscription") -> None:
        session = self.Session()
        session.execute(
            sa.delete(table.Subscription, table.Subscription.name == sub.name)
        )
        session.commit()

    def get_subscription(self, sub_name: str) -> "bgmi.core.Subscription":
        session = self.Session()
        row: table.Subscription = session.query(table.Subscription).filter_by(
            name=sub_name
        ).first()
        series = session.query(table.Series).filter_by(sub_name=sub_name)
        data = row.dict()
        data["series"] = [x.dict() for x in series]
        return bgmi.core.Subscription(**data)

    def save_subscription(self, sub: "bgmi.core.Subscription") -> None:
        self.add_subscription(sub)

    def get_all_subscription(
        self, filters: typing.Dict[str, typing.Any] = None
    ) -> typing.List["bgmi.core.Subscription"]:
        session = self.Session()
        subscriptions: typing.Dict[str, bgmi.core.Subscription] = {
            x.name: bgmi.core.Subscription(**x.dict())
            for x in session.query(table.Subscription).filter_by(**filters)
        }

        for x in session.query(table.Series).filter(
            table.Series.sub_name.in_([x.name for x in subscriptions.values()])
        ):
            subscriptions[x.sub_name].series.append(bgmi.core.Series(**x.dict()))

        return list(subscriptions.values())

    def get_series(self, source_id: str, name: str) -> "bgmi.core.Series":
        """todo

        :param source_id: source id
        :param name: series name
        """
