from http import HTTPStatus
from pathlib import Path

import pytest
import requests
from _pytest.config import Config
from pytest_docker.plugin import Services
from requests.exceptions import ConnectionError


# noinspection SpellCheckingInspection
@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: Config) -> str:
    return str(pytestconfig.rootdir / "docker-compose.test.yml")


@pytest.fixture(scope="session")
def server_url(docker_ip: str) -> str:
    # noinspection HttpUrlsUsage
    return f"http://{docker_ip}:80"


def is_responsive(url: str) -> bool:
    try:
        response = requests.get(url)
        if response.status_code == HTTPStatus.OK:
            return True
    except ConnectionError:
        pass
    return False


@pytest.fixture(scope="session", autouse=True)
def plugin_server(docker_services: Services, server_url: str):
    # noinspection SpellCheckingInspection
    url = f"{server_url}/ruok"
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return docker_services


@pytest.fixture()
def resources_folder() -> Path:
    return Path(__file__).parent / "resources"
