import io
from pathlib import Path
from typing import Any
from zipfile import BadZipfile

from fastapi import FastAPI, File, Response, UploadFile
from fastapi.responses import FileResponse
from lxml import etree

# noinspection PyProtectedMember
from lxml.etree import _ElementTree as ElementTree
from starlette.requests import Request
from starlette.responses import JSONResponse

from .plugin_manager import (
    add_new_jar_plugin,
    add_new_zip_plugin,
    remove_plugin_file,
    remove_plugin_xml,
    save_plugin_file,
    xml_parser,
)
from .settings import settings
from .utils import validate_extension

# TODO: change numbers to httpstatus
app = FastAPI()
plugins_tree: ElementTree = etree.parse(str(settings.plugins_xml), xml_parser)


# TODO: Can optimize the response size if we look at the build number and filter
# noinspection PyUnusedLocal
@app.get("/")
async def all_plugins(build: str) -> Response:
    return Response(
        content=etree.tostring(plugins_tree.getroot()), media_type="application/xml"
    )


@app.get("/get_plugin/{name}")
async def get_plugin(name: str):
    return FileResponse(settings.plugins_folder / name)


# TODO: add ability to delete plugin
# TODO: don't allow multiply copy of the same plugin
@app.post("/upload_jar", status_code=201)
async def upload(plugin: UploadFile = File(...)):
    filename = Path(plugin.filename)
    validate_extension(filename, ".jar")
    jar_data = await plugin.read()
    jar_data = jar_data if isinstance(jar_data, bytes) else jar_data.encode()
    jar_fileobject = io.BytesIO(jar_data)
    plugin_file_name = add_new_jar_plugin(plugins_tree, jar_fileobject, filename.name)
    save_plugin_file(plugin_file_name, jar_data)


@app.post("/upload_zip", status_code=201)
async def upload_zip(plugin_file: UploadFile = File(...)):
    file_name = Path(plugin_file.filename)
    validate_extension(file_name, ".zip")
    zip_data = await plugin_file.read()
    zip_data = zip_data if isinstance(zip_data, bytes) else zip_data.encode()
    zip_fileobject = io.BytesIO(zip_data)
    plugin_file_name = add_new_zip_plugin(plugins_tree, zip_fileobject, file_name)
    save_plugin_file(plugin_file_name, zip_data)


@app.delete("/", status_code=204, response_class=Response)
async def delete_plugin(plugin: str, version: str):
    plugin = remove_plugin_xml(plugins_tree, plugin, version)
    remove_plugin_file(settings.plugins_folder, plugin)


# noinspection PyUnusedLocal
@app.exception_handler(BadZipfile)
@app.exception_handler(ValueError)
async def value_exception_handler(request: Request, exc: Any):
    return JSONResponse(
        status_code=400,
        content={"exception": str(exc)},
    )
