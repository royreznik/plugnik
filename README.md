# PlugNik - Private plugin repository for JetBrains Applications
![licesns](https://img.shields.io/github/license/royreznik/plugnik)
![python](https://img.shields.io/badge/python-v3.9-blue)
![code style](https://camo.githubusercontent.com/d91ed7ac7abbd5a6102cbe988dd8e9ac21bde0a73d97be7603b891ad08ce3479/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c61636b2d3030303030302e737667)
![lastcommit](https://img.shields.io/github/last-commit/royreznik/plugnik)
![tests](https://github.com/royreznik/plugnik/actions/workflows/CI.yml/badge.svg)
![imagee size](https://img.shields.io/docker/image-size/royreznik/plugnik)
![docker pulls](https://img.shields.io/docker/pulls/royreznik/plugnik)

PlugNik is a simple implementation of plugin repository for JetBrains Application.

The server is completely stands alone, and can easily be deployed on any environment!


## Running
```bash
make run
```

## Developing
```bash
make install
make run-dev 
```
in development mode the server code is mounted into the container, 
and `uvicorn` is set to reload mode, which allow you to run the server inside the container and keep developing!

## How to Use
Instruction about how to add the repository to your application can be found in
JetBrains official documentation [here](https://www.jetbrains.com/help/idea/managing-plugins.html#repos)

## How to upload plugins
Navigate into `http://server-url/upload` and you will have a simple drag&drop for plugins!

## Docker Image
```bash
docker pull royreznik/plugnik:alpha
```
