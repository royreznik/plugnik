import zipfile
from pathlib import Path
from typing import IO

from lxml import etree
from lxml.etree import _ElementTree as ElementTree

xml_parser = etree.XMLParser(remove_blank_text=True)


def add_new_zip_plugin(
    plugins_tree: ElementTree, zip_fileobject: IO, zip_name: Path, plugin_file_name: str
) -> None:
    zip_file = zipfile.ZipFile(zip_fileobject)
    jar_plugin_name = zip_name.with_suffix(".jar").name
    jar_plugin_path = [i for i in zip_file.namelist() if jar_plugin_name in i][0]
    add_new_jar_plugin(plugins_tree, zip_file.open(jar_plugin_path), plugin_file_name)


def add_new_jar_plugin(
    plugins_tree: ElementTree, jar_fileobject: IO, plugin_file_name: str
) -> None:
    plugin_metadata = _get_plugin_metadata_from_jar(jar_fileobject)
    new_plugin_xml = _generate_plugin_xml_from_metadata(
        plugin_metadata, plugin_file_name
    )
    _dump_new_plugin(plugins_tree, new_plugin_xml)


def _get_plugin_metadata_from_jar(jar_fileobject: IO) -> ElementTree:
    jar = zipfile.ZipFile(jar_fileobject, "r")

    if "META-INF/plugin.xml" not in jar.namelist():
        raise ValueError("Couldn't find plugin.xml file inside the jar")

    with jar.open("META-INF/plugin.xml") as metadata_file:
        return etree.parse(metadata_file, xml_parser).getroot()


def _generate_plugin_xml_from_metadata(
    plugin_metadata: ElementTree, plugin_file_name: str
) -> ElementTree:
    # noinspection PyUnresolvedReferences
    new_plugin_xml = etree.Element(
        "plugin",
        attrib={
            "id": plugin_metadata.find("id").text,
            "url": "/get_plugin/" + plugin_file_name,  # TODO: Make this better
            "version": plugin_metadata.find("version").text,
        },
    )
    new_plugin_xml.append(plugin_metadata.find("idea-version"))
    new_plugin_xml.append(plugin_metadata.find("name"))
    return new_plugin_xml


def _dump_new_plugin(plugins_tree: ElementTree, new_plugin_xml: ElementTree) -> None:
    # noinspection PyUnresolvedReferences
    plugins_tree.getroot().append(new_plugin_xml)
    plugins_tree.write("/updatePlugins.xml", pretty_print=True)
