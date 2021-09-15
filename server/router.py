import io
from pathlib import Path

from fastapi import FastAPI, Response, UploadFile, File, HTTPException
from lxml import etree
from lxml.etree import _ElementTree as ElementTree

from .utils import xml_parser, add_new_plugin

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


# TODO: delete plugin if fail
# TODO: add ability to delete plugin
@app.post("/upload", status_code=201)
async def upload(plugin: UploadFile = File(...)):
    filename = Path(plugin.filename)
    if not filename.suffix == ".jar":
        raise HTTPException(status_code=400, detail="You must upload a .jar file!")
    jar_data = await plugin.read()
    jar_fileobject = io.BytesIO(jar_data)
    jar_location = plugins_folder / filename.name
    try:
        add_new_plugin(plugins_tree, jar_fileobject, jar_location)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    jar_location.write_bytes(jar_data)
