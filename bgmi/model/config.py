import enum
import os
import platform
import secrets
import string
import tempfile
from typing import Dict, List

from pydantic import BaseSettings, Extra


class DownloadDelegateEnum(str, enum.Enum):
    def __str__(self) -> str:
        return self.value


def get_bgmi_path() -> str:
    p = os.path.normpath(os.environ.get("BGMI_PATH", os.path.expanduser("~/.bgmi")))
    if not p:
        p = tempfile.mkdtemp()
        print("$HOME and $BGMI_PATH not set, use a tmp dir " + p)
    return p


def gen_password(length: int) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


class WritableConfig(BaseSettings):
    output: Dict[str, dict] = {}
    source: Dict[str, dict] = {}
    strainer: Dict[str, dict] = {"keywords weight": {"1080": 10, "720": 5}}
    backend: dict = {}
    disabled_source: List[str] = []
    # enable global filter

    # Global blocked keyword
    # global_keyword_filter: List[str] = [
    #     "Leopard-Raws",
    #     "hevc",
    #     "x265",
    #     "c-a Raws",
    #     "U3-Web",
    # ]
    # enable_global_filter: bool = True

    # use tornado serving video files

    logger: dict = {}  #: will be parsed by ``logging.config.dictConfig``

    bgmi_path: str = get_bgmi_path()
    save_path: str = os.path.join(bgmi_path, "bangumi")

    class Config:
        env_prefix = "BGMI_"
        extra = Extra.ignore


class Config(WritableConfig):
    """user defined in ``$BGMI_PATH/bgmi.cfg``"""

    # DB_PATH: str = os.path.join(BGMI_PATH, 'bangumi.db')

    is_windows = platform.system() == "Windows"
    show_warning = bool(os.getenv("DEV") or os.getenv("DEBUG"))
    #: path of bgmi path, not project path
    src_root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

    @property
    def db_path(self) -> str:
        return os.path.join(self.bgmi_path, "bangumi.db")

    @property
    def config_file_path(self) -> str:
        return os.path.join(self.bgmi_path, "bgmi.cfg")

    @property
    def tools_path(self) -> str:
        return os.path.join(self.bgmi_path, "tools")

    @property
    def tmp_path(self) -> str:
        return os.path.join(self.bgmi_path, "tmp")


if __name__ == "__main__":
    import toml

    print(
        os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "examples", "config.toml")
        )
    )
    with open(
        os.path.join(os.path.dirname(__file__), "../..", "examples", "config.toml")
    ) as f:
        print(toml.load(f))
