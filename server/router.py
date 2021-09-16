import io
from pathlib import Path
from typing import Any
from zipfile import BadZipfile

from fastapi import FastAPI, File, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse
from lxml import etree

# noinspection PyProtectedMember
from lxml.etree import _ElementTree as ElementTree
from starlette.requests import Request
from starlette.responses import JSONResponse

from .settings import settings
from .plugin_manager import add_new_jar_plugin, add_new_zip_plugin, xml_parser

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
@app.post("/upload_jar", status_code=201)
async def upload(plugin: UploadFile = File(...)):
    filename = Path(plugin.filename)
    if not filename.suffix == ".jar":
        raise HTTPException(status_code=400, detail="You must upload a .jar file!")
    jar_data = await plugin.read()
    if isinstance(jar_data, str):
        jar_data = jar_data.encode()
    jar_fileobject = io.BytesIO(jar_data)
    plugin_file_name = add_new_jar_plugin(plugins_tree, jar_fileobject, filename.name)
    (settings.plugins_folder / plugin_file_name).write_bytes(jar_data)


@app.post("/upload_zip", status_code=201)
async def upload_zip(plugin: UploadFile = File(...)):
    filename = Path(plugin.filename)
    if not filename.suffix == ".zip":
        raise HTTPException(status_code=400, detail="You must upload a .zip file!")

    zip_data = await plugin.read()
    if isinstance(zip_data, str):
        zip_data = zip_data.encode()
    zip_fileobject = io.BytesIO(zip_data)
    plugin_file_name = add_new_zip_plugin(plugins_tree, zip_fileobject, filename)
    (settings.plugins_folder / plugin_file_name).write_bytes(zip_data)


# noinspection PyUnusedLocal
@app.exception_handler(BadZipfile)
@app.exception_handler(ValueError)
async def value_exception_handler(request: Request, exc: Any):
    return JSONResponse(
        status_code=400,
        content={"exception": str(exc)},
    )
