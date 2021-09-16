import zipfile
from pathlib import Path
from typing import IO

from lxml import etree

# noinspection PyProtectedMember
from lxml.etree import _Element as Element
from lxml.etree import _ElementTree as ElementTree

from .settings import plugin_manager_settings

xml_parser = etree.XMLParser(remove_blank_text=True)
plugins_tree: ElementTree = etree.parse(str(plugin_manager_settings.plugins_xml), xml_parser)


def remove_plugin_xml(
    plugin_name: str, version: str
) -> Element:
    plugin_search_query = (
        f'.//plugin[@version="{version}"]//name[text()="{plugin_name}"]'
    )
    plugin_search_result = plugins_tree.getroot().xpath(plugin_search_query)

    if not plugin_search_result:
        raise ValueError(f"Plugin not found. name: {plugin_name}, version: {version}")
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


def get_all_plugins_xml_string() -> str:
    return etree.tostring(plugins_tree.getroot())


def add_new_zip_plugin(
    zip_fileobject: IO, zip_name: Path
) -> str:
    plugin_archive = zipfile.ZipFile(zip_fileobject)
    inner_jar_name = zip_name.with_suffix(".jar").name
    inner_jar_path = [i for i in plugin_archive.namelist() if inner_jar_name in i][0]
    return add_new_jar_plugin(
        plugin_archive.open(inner_jar_path), zip_name.name
    )


def add_new_jar_plugin(
    jar_fileobject: IO, plugin_file_name: str
) -> str:
    plugin_metadata = _get_plugin_metadata_from_jar(jar_fileobject)
    plugin_version = plugin_metadata.find("version").text
    plugin_file_name = f"{plugin_version}-{plugin_file_name}"  # Refactor this shit
    new_plugin_xml = _generate_plugin_xml_from_metadata(
        plugin_metadata, plugin_file_name, plugin_version
    )
    _dump_new_plugin_xml(new_plugin_xml)
    return plugin_file_name


def _get_plugin_metadata_from_jar(jar_fileobject: IO) -> ElementTree:
    jar = zipfile.ZipFile(jar_fileobject, "r")

    if "META-INF/plugin.xml" not in jar.namelist():
        raise ValueError("Couldn't find plugin.xml file inside the jar")

    with jar.open("META-INF/plugin.xml") as metadata_file:
        return etree.parse(metadata_file, xml_parser).getroot()


def _generate_plugin_xml_from_metadata(
    plugin_metadata: ElementTree, plugin_file_name: str, plugin_version: str
) -> ElementTree:
    # noinspection PyUnresolvedReferences
    new_plugin_xml = etree.Element(
        "plugin",
        attrib={
            "id": plugin_metadata.find("id").text,
            "url": f"/get_plugin/{plugin_file_name}",  # TODO: Make this better
            "version": plugin_version,
        },
    )
    new_plugin_xml.append(plugin_metadata.find("idea-version"))
    new_plugin_xml.append(plugin_metadata.find("name"))
    return new_plugin_xml


def _dump_new_plugin_xml(
    new_plugin_xml: ElementTree
) -> None:
    # noinspection PyUnresolvedReferences
    plugins_tree.getroot().append(new_plugin_xml)
    plugins_tree.write(str(plugin_manager_settings.plugins_xml), pretty_print=True)
