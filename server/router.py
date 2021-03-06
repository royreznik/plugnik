import io
from http import HTTPStatus
from pathlib import Path
from typing import Any, List
from zipfile import BadZipfile

from fastapi import FastAPI, File, Request, Response, UploadFile
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from .plugin_manager import (
    add_new_jar_plugin,
    add_new_zip_plugin,
    get_all_plugins_xml_string,
    get_plugin_file_path,
    remove_plugin_file,
    remove_plugin_xml,
    save_plugin_file,
)
from .utils import validate_allowed_extensions

app = FastAPI()

app.mount("/static", StaticFiles(directory="server/static"), name="static")


# TODO: Can optimize the response size if we look at the build number and filter
# noinspection PyUnusedLocal
@app.get("/")
async def all_plugins(build: str) -> Response:
    return Response(content=get_all_plugins_xml_string(), media_type="application/xml")


@app.get("/get_plugin/{name}")
async def get_plugin(name: str):
    return FileResponse(get_plugin_file_path(name))


@app.post("/upload", status_code=HTTPStatus.CREATED)
async def upload(plugin_files: List[UploadFile] = File(...)):
    for plugin_file in plugin_files:
        file_name = Path(plugin_file.filename)
        validate_allowed_extensions(file_name)
        plugin_data = await plugin_file.read()
        plugin_data = (
            plugin_data if isinstance(plugin_data, bytes) else plugin_data.encode()
        )
        plugin_fileobject = io.BytesIO(plugin_data)
        plugin_file_name = (
            add_new_zip_plugin(plugin_fileobject, file_name)
            if file_name.suffix == ".zip"
            else add_new_jar_plugin(plugin_fileobject, file_name.name)
        )
        save_plugin_file(plugin_file_name, plugin_data)


@app.get("/upload")
async def redirect_upload() -> RedirectResponse:
    return RedirectResponse("/static/upload.html")


@app.get("/favicon.ico")
async def redirect_favicon() -> RedirectResponse:
    return RedirectResponse("/static/favicon.ico")


@app.delete("/", status_code=HTTPStatus.NO_CONTENT, response_class=Response)
async def delete_plugin(plugin: str, version: str):
    plugin = remove_plugin_xml(plugin, version)
    remove_plugin_file(plugin)


# noinspection SpellCheckingInspection
@app.get("/ruok", status_code=HTTPStatus.OK, response_class=Response)
def ruok() -> str:
    return "imok"


# noinspection PyUnusedLocal
@app.exception_handler(BadZipfile)
@app.exception_handler(ValueError)
async def value_exception_handler(request: Request, exc: Any):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={"exception": str(exc)},
    )


# noinspection PyUnusedLocal
@app.exception_handler(KeyError)
async def key_exception_handler(request: Request, exc: Any):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"exception": str(exc)},
    )
