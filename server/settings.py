import json
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    plugins_xml: Path = Path("/updatePlugins.xml")
    plugins_folder: Path = Path("/tmp/plugins/")


with open("/app/settings.json") as f:
    settings = Settings(**json.load(f))
