import zipfile
from pathlib import Path
from typing import IO

from lxml import etree
from lxml.etree import _Element as Element  # noqa
from lxml.etree import _ElementTree as ElementTree  # noqa

from .settings import plugin_manager_settings

xml_parser = etree.XMLParser(remove_blank_text=True)
plugins_tree: ElementTree = etree.parse(
    str(plugin_manager_settings.plugins_xml), xml_parser
)


def remove_plugin_xml(plugin_name: str, version: str) -> Element:
    plugin_search_query = (
        f'.//plugin[@version="{version}"]//name[text()="{plugin_name}"]'
    )
    plugin_search_result = plugins_tree.getroot().xpath(plugin_search_query)

    if not plugin_search_result:
        raise KeyError(f"Plugin not found. name: {plugin_name}, version: {version}")
    plugin = plugin_search_result[0].getparent()
    plugins_tree.getroot().remove(plugin)
    plugins_tree.write(str(plugin_manager_settings.plugins_xml), pretty_print=True)
    return plugin


def remove_plugin_file(plugin: Element) -> None:
    plugin_url = plugin.attrib["url"]
    plugin_file_name = Path(plugin_url).name
    (plugin_manager_settings.plugins_folder / plugin_file_name).unlink(missing_ok=True)


def save_plugin_file(plugin_file_name: str, plugin_data: bytes):
    (plugin_manager_settings.plugins_folder / plugin_file_name).write_bytes(plugin_data)


def get_plugin_file_path(name: str) -> Path:
    return plugin_manager_settings.plugins_folder / name


def get_all_plugins_xml_string() -> bytes:
    return bytes(etree.tostring(plugins_tree.getroot()))


def add_new_zip_plugin(zip_fileobject: IO, zip_name: Path) -> str:
    plugin_archive = zipfile.ZipFile(zip_fileobject)
    inner_jar_path = _find_jar_plugin(plugin_archive)
    return add_new_jar_plugin(plugin_archive.open(inner_jar_path), zip_name.name)


def _find_jar_plugin(zip_file: zipfile.ZipFile) -> str:
    inner_jars = [i for i in zip_file.namelist() if Path(i).suffix == ".jar"]
    for jar in inner_jars:
        try:
            with zip_file.open(jar) as inner_jar:
                with zipfile.ZipFile(inner_jar) as inner_jar_file:
                    if "META-INF/plugin.xml" in inner_jar_file.namelist():
                        return jar
        except zipfile.BadZipfile:
            pass
    raise ValueError("Couldn't find plugin.xml file inside the jar")


def add_new_jar_plugin(jar_fileobject: IO, plugin_file_name: str) -> str:
    plugin_metadata = _get_plugin_metadata_from_jar(jar_fileobject)
    plugin_version = plugin_metadata.find("version").text
    plugin_file_name = f"{plugin_version}-{plugin_file_name}"  # Refactor this shit
    new_plugin_xml = _generate_plugin_xml_from_metadata(
        plugin_metadata, plugin_file_name, plugin_version
    )
    _validate_plugin_not_exists(new_plugin_xml)
    _dump_new_plugin_xml(new_plugin_xml)
    return plugin_file_name


def _get_plugin_metadata_from_jar(jar_fileobject: IO) -> Element:
    jar = zipfile.ZipFile(jar_fileobject, "r")

    if "META-INF/plugin.xml" not in jar.namelist():
        raise ValueError("Couldn't find plugin.xml file inside the jar")

    with jar.open("META-INF/plugin.xml") as metadata_file:
        return etree.parse(metadata_file, xml_parser).getroot()


def _generate_plugin_xml_from_metadata(
    plugin_metadata: Element, plugin_file_name: str, plugin_version: str
) -> Element:
    # noinspection PyUnresolvedReferences
    plugin_name = plugin_metadata.find("name")
    plugin_id = plugin_metadata.find("id")
    plugin_id = plugin_id if plugin_id is not None else plugin_name
    new_plugin_xml = etree.Element(
        "plugin",
        attrib={
            "id": plugin_id.text,
            "url": f"/get_plugin/{plugin_file_name}",  # TODO: Make this better
            "version": plugin_version,
        },
    )
    new_plugin_xml.append(plugin_metadata.find("idea-version"))
    new_plugin_xml.append(plugin_name)
    return new_plugin_xml


def _dump_new_plugin_xml(new_plugin_xml: Element) -> None:
    # noinspection PyUnresolvedReferences
    plugins_tree.getroot().append(new_plugin_xml)
    plugins_tree.write(str(plugin_manager_settings.plugins_xml), pretty_print=True)


def _validate_plugin_not_exists(new_plugin_xml: Element):
    if etree.tostring(new_plugin_xml) in etree.tostring(plugins_tree):
        raise ValueError("This plugin already exists!")
