import os
import sqlite3
import typing
from contextlib import contextmanager
from os import path

import sqlalchemy as sa
import sqlalchemy.exc
from alembic import command
from alembic.config import Config
from pydantic import BaseSettings, ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import bgmi.core
from bgmi import db
from bgmi.db import table
from bgmi.exc import ConfigNotValid, SeriesNotFollowed
from bgmi.protocol import backend


class SqliteConfig(BaseSettings):
    db_path: str = os.path.expanduser("~/.bgmi/app.db")


class SQLiteBackend(backend.Base):
    version = "0.0.1"
    cfg: SqliteConfig

    def create_engine(self) -> sa.engine.base.Engine:
        return create_engine("sqlite:///" + self.cfg.db_path)

    @staticmethod
    def parse_config(config: dict) -> SqliteConfig:
        try:
            return SqliteConfig.parse_obj(config)
        except ValidationError as e:
            raise ConfigNotValid() from e

    @classmethod
    def install(cls, config: dict) -> None:
        cfg = cls.parse_config(config)
        alembic_config = Config(path.join(path.dirname(__file__), "alembic.ini"))
        alembic_config.set_main_option("sqlalchemy.url", "sqlite:///" + cfg.db_path)
        command.upgrade(alembic_config, "head")

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.cfg = self.parse_config(config)
        self.Session = sessionmaker(self.create_engine())

    @contextmanager
    def get_session(self) -> Session:
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

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
        with self.get_session() as session:
            session.execute(
                sa.delete(table.Subscription, table.Subscription.name == sub.name)
            )

    def get_subscription(self, sub_name: str) -> "bgmi.core.Subscription":
        with self.get_session() as session:
            row: table.Subscription = session.query(table.Subscription).filter_by(
                name=sub_name
            ).first()
            series: typing.List[table.Series] = session.query(table.Series).filter_by(
                sub_name=sub_name
            ).all()
            data = row.dict()
            data["series"] = [x.to_core_obj() for x in series]
        return bgmi.core.Subscription(**data)

    def save_subscription(self, sub: "bgmi.core.Subscription") -> None:
        self.add_subscription(sub)

    def get_all_subscription(
        self, filters: typing.Dict[str, typing.Any] = None
    ) -> typing.List["bgmi.core.Subscription"]:
        if filters is None:
            filters = {}

        with self.get_session() as session:
            subscriptions: typing.Dict[str, bgmi.core.Subscription] = {
                x.name: bgmi.core.Subscription(**x.dict())
                for x in session.query(table.Subscription).filter_by(**filters)
            }

            for x in session.query(table.Series).filter(
                table.Series.sub_name.in_([x.name for x in subscriptions.values()])
            ):
                subscriptions[x.sub_name].series.append(x.to_core_obj())

        return list(subscriptions.values())

    def get_series(self, source_id: str, name: str) -> "bgmi.core.Series":
        """todo

        :param source_id: source id
        :param name: series name
        """
        with self.get_session() as session:
            s: typing.Optional[table.Series] = (
                session.query(table.Series)
                .filter(table.Series.source == source_id, table.Series.name == name)
                .first()
            )
            if s is None:
                raise SeriesNotFollowed(
                    f"can't find series {name} in source {source_id}"
                )
            return s.to_core_obj()


if __name__ == "__main__":
    SQLiteBackend.install({"db_path": os.path.expanduser("./tmp/test.db")})
