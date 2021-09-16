import json
from pathlib import Path

from pydantic import BaseSettings


class PluginManagerSettings(BaseSettings):
    plugins_xml: Path = Path("/updatePlugins.xml")
    plugins_folder: Path = Path("/tmp/plugins/")


with open("/app/settings/plugin_manager.json") as f:
    plugin_manager_settings = PluginManagerSettings(**json.load(f))
