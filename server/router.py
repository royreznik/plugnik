import io
import zipfile
from pathlib import Path

from fastapi import FastAPI, Response, UploadFile, File, HTTPException
from lxml import etree
from lxml.etree import _ElementTree as ElementTree
from fastapi.responses import FileResponse
from .utils import xml_parser, add_new_jar_plugin, add_new_zip_plugin

app = FastAPI()
# TODO: Extract to config
# TODO: create the file if not exists
plugins_tree: ElementTree = etree.parse("updatePlugins.xml", xml_parser)
plugins_folder = Path("/tmp/plugins/")


@app.get("/")
async def all_plugins(build: str) -> Response:
    return Response(
        content=etree.tostring(plugins_tree.getroot()), media_type="application/xml"
    )


@app.get("/get_plugin/{name}")
async def get_plugin(name: str):
    return FileResponse(plugins_folder / name)


# TODO: add handler for value error
# TODO: delete plugin if fail
# TODO: add ability to delete plugin
@app.post("/upload_jar", status_code=201)
async def upload(plugin: UploadFile = File(...)):
    filename = Path(plugin.filename)
    if not filename.suffix == ".jar":
        raise HTTPException(status_code=400, detail="You must upload a .jar file!")
    jar_data = await plugin.read()
    jar_fileobject = io.BytesIO(jar_data)
    add_new_jar_plugin(plugins_tree, jar_fileobject, filename.name)
    (plugins_folder / filename.name).write_bytes(jar_data)


@app.post("/upload_zip", status_code=201)
async def upload_zip(plugin: UploadFile = File(...)):
    filename = Path(plugin.filename)
    if not filename.suffix == ".zip":
        raise HTTPException(status_code=400, detail="You must upload a .zip file!")

    zip_data = await plugin.read()
    zip_fileobject = io.BytesIO(zip_data)
    add_new_zip_plugin(plugins_tree, zip_fileobject, filename, filename.name)
    (plugins_folder / filename.name).write_bytes(zip_data)
