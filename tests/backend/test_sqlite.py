import os
import os.path
import sqlite3
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture

from bgmi.backend.sqlite import SQLiteBackend, SqliteConfig
from bgmi.core import Subscription
from bgmi.exc import ConfigNotValid, SeriesNotFollowed


@pytest.fixture
def sqlite_db_config(tmpdir):
    yield SqliteConfig.parse_obj({"db_path": os.path.join(tmpdir, "test.db")})


@pytest.fixture
def sqlite_backend(sqlite_db_config):
    SQLiteBackend.install(sqlite_db_config.dict())
    yield SQLiteBackend(sqlite_db_config.dict())


def test_install(sqlite_db_config: SqliteConfig):
    SQLiteBackend.install(sqlite_db_config.dict())
    conn = sqlite3.connect(sqlite_db_config.db_path)
    tables = conn.execute(
        "SELECT Name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    assert tables


def test_add_subscription(sqlite_backend: SQLiteBackend):
    sqlite_backend.add_subscription(
        Subscription(name="233", updating=False, episode=10)
    )
    with sqlite3.connect(sqlite_backend.cfg.db_path) as conn:
        sub = conn.execute(
            "select name, episode, updating from subscription where name='233'"
        ).fetchone()
        assert sub == ("233", 10, False), "subscription in db diff from args"


def test_add_subscription_exists(sqlite_backend: SQLiteBackend):
    with sqlite3.connect(sqlite_backend.cfg.db_path) as conn:
        conn.execute("insert into subscription(name, episode) values ('233', 2)")

    sqlite_backend.add_subscription(
        Subscription(name="233", updating=False, episode=10)
    )

    with sqlite3.connect(sqlite_backend.cfg.db_path) as conn:
        sub = conn.execute(
            "select episode from subscription where name='233'"
        ).fetchone()
        assert sub[0] == 10, "existed subscription should be replaced by args"


def test_remove_subscription(sqlite_backend: SQLiteBackend):
    with sqlite3.connect(sqlite_backend.cfg.db_path) as conn:
        conn.execute("insert into subscription(name, episode) values ('233', 2)")

    sqlite_backend.remove_subscription(Subscription(name="233"))

    with sqlite3.connect(sqlite_backend.cfg.db_path) as conn:
        sub = conn.execute("select * from subscription where name='233'").fetchone()
        assert sub is None, "subscription should be deleted"


def test_get_subscription(sqlite_backend: SQLiteBackend):
    with sqlite3.connect(sqlite_backend.cfg.db_path) as conn:
        conn.execute(
            "insert into subscription(name, episode, updating) values ('233', 2, 1)"
        )

    sub = sqlite_backend.get_subscription("233")
    assert (sub.name, sub.episode, sub.updating) == (
        "233",
        2,
        True,
    ), "subscription not same with db record"


def test_get_subscription_with_series(sqlite_backend: SQLiteBackend):
    with sqlite3.connect(sqlite_backend.cfg.db_path) as conn:
        conn.execute(
            "insert into subscription(name, episode, updating) "
            "values ('233', 2, 1), ('234', 3, 0)"
        )
        conn.execute(
            "insert into series(id, name, source, sub_name)"
            " values ('id1','n', 'src', '233'), ('id2', 'm','c','234')"
        )

    s = sqlite_backend.get_subscription("233")
    assert len(s.series) == 1, "subscription get extra series"
    assert s.series[0].id == "id1", "subscription get wrong series"


def test_save_subscription(mocker: MockFixture, sqlite_db_config):
    m: MagicMock = mocker.patch("bgmi.backend.sqlite.SQLiteBackend.add_subscription")
    sub = Subscription(name="233")
    SQLiteBackend(sqlite_db_config).save_subscription(sub)
    m.assert_called_once_with(sub)


def test_get_all_subscription(sqlite_backend: SQLiteBackend):
    with sqlite3.connect(sqlite_backend.cfg.db_path) as conn:
        conn.execute(
            "insert into subscription(name, episode, updating) values ('233', 2, 1), "
            "('234',3,0)"
        )
    s = sqlite_backend.get_all_subscription()
    assert len(s) == 2


def test_get_all_subscription_filter(sqlite_backend: SQLiteBackend):
    with sqlite3.connect(sqlite_backend.cfg.db_path) as conn:
        conn.execute(
            "insert into subscription(name, episode, updating) values ('233', 2, 1), "
            "('234',3,0)"
        )

    s = sqlite_backend.get_all_subscription(filters={"name": "233"})
    assert len(s) == 1
    assert s[0].name == "233"


def test_get_all_subscription_with_series(sqlite_backend: SQLiteBackend):
    with sqlite3.connect(sqlite_backend.cfg.db_path) as conn:
        conn.execute(
            "insert into subscription(name, episode, updating) "
            "values ('233', 2, 1), ('234', 3, 0)"
        )
        conn.execute(
            "insert into series(id, name, source, sub_name)"
            " values ('id1','n', 'src', '233'), ('id2', 'm','c','234')"
        )

    sub_list = sqlite_backend.get_all_subscription({"name": "233"})
    assert sub_list
    s = sub_list[0]
    assert len(s.series) == 1, "subscription get extra series"
    assert s.series[0].id == "id1", "subscription get wrong series"


def test_get_series(sqlite_backend: SQLiteBackend):
    with sqlite3.connect(sqlite_backend.cfg.db_path) as conn:
        conn.execute(
            "insert into series(id, name, source, sub_name)"
            " values ('id1','n', 'src', '233'), ('id2', 'm','c','234')"
        )
    s = sqlite_backend.get_series("src", "n")
    assert s.id == "id1", "sqlite_backend.get_series get wrong series"


def test_get_series_raise(sqlite_backend: SQLiteBackend):
    with pytest.raises(SeriesNotFollowed):
        sqlite_backend.get_series("1", "2")


def test_wrong_config():
    with pytest.raises(ConfigNotValid):
        SQLiteBackend({"a": "b"})


def test_impl_all_abstract_method():
    SQLiteBackend({})
