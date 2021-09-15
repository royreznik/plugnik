import zipfile
from pathlib import Path
from typing import IO
from lxml import etree
from lxml.etree import _ElementTree as ElementTree, XMLParser

xml_parser = etree.XMLParser(remove_blank_text=True)


def add_new_plugin(
    plugins_tree: ElementTree, jar_fileobject: IO, jar_location: Path
) -> None:
    plugin_metadata = _get_plugin_metadata_from_jar(jar_fileobject)
    new_plugin_xml = _generate_plugin_xml_from_metadata(plugin_metadata, jar_location)
    _dump_new_plugin(plugins_tree, new_plugin_xml)


def _get_plugin_metadata_from_jar(jar_fileobject: IO) -> ElementTree:
    jar = zipfile.ZipFile(jar_fileobject, "r")

    if not "META-INF/plugin.xml" in jar.namelist():
        raise ValueError("Couldn't find plugin.xml file inside the jar")

    with jar.open("META-INF/plugin.xml") as metadata_file:
        return etree.parse(metadata_file, xml_parser).getroot()


def _generate_plugin_xml_from_metadata(
    plugin_metadata: ElementTree, jar_location: Path
) -> ElementTree:
    # noinspection PyUnresolvedReferences
    new_plugin_xml = etree.Element(
        "plugin",
        attrib={
            "id": plugin_metadata.find("id").text,
            "url": str(jar_location),
            "version": plugin_metadata.find("version").text,
        },
    )
    new_plugin_xml.append(plugin_metadata.find("idea-version"))
    new_plugin_xml.append(plugin_metadata.find("name"))
    return new_plugin_xml


def _dump_new_plugin(plugins_tree: ElementTree, new_plugin_xml: ElementTree) -> None:
    # noinspection PyUnresolvedReferences
    plugins_tree.getroot().append(new_plugin_xml)
    plugins_tree.write("updatePlugins.xml", pretty_print=True)
