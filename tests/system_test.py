import io
from http import HTTPStatus
from pathlib import Path
from typing import Optional, Tuple

import pytest
import requests
from requests import Response


@pytest.mark.parametrize(["extension"], [["zip"], ["jar"]])
def test_upload_get_delete(
    resources_folder: Path, server_url: str, extension: str
) -> None:

    plugins_xml = requests.get(f"{server_url}/?build=").text
    assert plugins_xml == "<plugins/>"

    upload_response, plugin_data = upload_resource_plugin(
        server_url, resources_folder, f"plugin.{extension}"
    )

    assert upload_response.status_code == HTTPStatus.CREATED, upload_response.text

    # noinspection SpellCheckingInspection
    expected_plugin_xml = (
        f'<plugin id="rez.nik" url="/get_plugin/1-plugin.{extension}" version="1">'
        f'<idea-version since-build="192"/>'
        f"<name>Reznik</name>"
        f"</plugin>"
    )

    plugins_xml = requests.get(f"{server_url}/?build=").text
    assert expected_plugin_xml in plugins_xml

    plugin_from_server = requests.get(
        f"{server_url}/get_plugin/1-plugin.{extension}"
    ).content
    assert plugin_from_server == plugin_data

    # noinspection SpellCheckingInspection
    delete_response = requests.delete(f"{server_url}/?plugin=Reznik&version=1")
    assert delete_response.status_code == HTTPStatus.NO_CONTENT, delete_response.text

    plugins_xml = requests.get("http://localhost:80/?build=").text
    assert plugins_xml == "<plugins/>"


def test_delete_plugin_that_does_not_exist(server_url: str) -> None:
    # noinspection SpellCheckingInspection
    delete_response = requests.delete(f"{server_url}/?plugin=Kuku&version=1")
    assert delete_response.status_code == HTTPStatus.NOT_FOUND, delete_response.text


@pytest.mark.parametrize(["extension"], [["zip"], ["jar"]])
def test_upload_file_with_different_extension(
    server_url: str, resources_folder: Path, extension: str
):
    upload_response, _ = upload_resource_plugin(
        server_url,
        resources_folder,
        f"plugin.{extension}",
        "plugin.exe",
    )
    assert upload_response.status_code == HTTPStatus.BAD_REQUEST, upload_response.text


@pytest.mark.parametrize(["extension"], [["zip"], ["jar"]])
def test_upload_wrong_file_type(
    server_url: str, resources_folder: Path, extension: str
):
    upload_response, _ = upload_resource_plugin(
        server_url,
        resources_folder,
        f"fake_{extension}.{extension}",
    )
    assert upload_response.status_code == HTTPStatus.BAD_REQUEST, upload_response.text


def test_upload_jar_that_is_not_a_plugin(server_url: str, resources_folder: Path):
    upload_response, _ = upload_resource_plugin(
        server_url, resources_folder, "not_plugin.jar"
    )
    assert upload_response.status_code == HTTPStatus.BAD_REQUEST, upload_response.text


def test_upload_two_plugins_once(server_url: str, resources_folder: Path):
    with open(resources_folder / "plugin.jar", "rb") as j, open(
        resources_folder / "plugin.zip", "rb"
    ) as z:
        jar_data = j.read()
        zip_data = z.read()
        files = [
            ("plugin_files", ("plugin.jar", io.BytesIO(jar_data))),
            ("plugin_files", ("plugin.zip", io.BytesIO(zip_data))),
        ]
    upload_response = requests.post(f"{server_url}/upload", files=files)

    assert upload_response.status_code == HTTPStatus.CREATED, upload_response.text
    plugins_xml = requests.get(f"{server_url}/?build=").text

    expected_plugin_xml = (
        '<plugin id="rez.nik" url="/get_plugin/1-plugin.jar" version="1">'
        '<idea-version since-build="192"/>'
        "<name>Reznik</name>"
        "</plugin>"
        '<plugin id="rez.nik" url="/get_plugin/1-plugin.zip" version="1">'
        '<idea-version since-build="192"/>'
        "<name>Reznik</name>"
        "</plugin>"
    )

    assert expected_plugin_xml in plugins_xml


@pytest.mark.parametrize(
    ("plugin_name"),
    (
        ("Docker-213.4250.391.zip"),
        ("go-213.4631.20.zip"),
        ("IdeaVim-1.7.2.zip"),
        ("intellij-rainbow-brackets-6.21.zip"),
        ("js-karma-213.4631.9.zip"),
        ("Key-Promoter-X-2021.2.zip"),
        ("makefile-213.4250.391.zip"),
        ("poetry-pycharm-plugin.zip"),
        ("python-213.4631.20.zip"),
        ("StringManipulation.zip"),
    ),
)
def test_upload_real_plugins(server_url: str, real_plugins_folder: Path, plugin_name: str):
    upload_response, plugin_data = upload_resource_plugin(
        server_url, real_plugins_folder, plugin_name
    )
    assert upload_response.status_code == HTTPStatus.CREATED, upload_response.text


def upload_resource_plugin(
    server_url: str,
    resources_folder: Path,
    file_name: str,
    server_file_name: Optional[str] = None,
) -> Tuple[Response, bytes]:
    server_file_name = server_file_name or file_name
    plugin_path = resources_folder / file_name
    with open(plugin_path, "rb") as f:
        plugin_data = f.read()
    upload_response = requests.post(
        f"{server_url}/upload",
        files=[
            ("plugin_files", (server_file_name, io.BytesIO(plugin_data))),
        ],
    )
    return upload_response, plugin_data
