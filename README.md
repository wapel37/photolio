# Photolio

*Photolio is nothing more than just the simplest form of photographer portfolio
...self-hosted, so even better!*

## Config
Stored in: `./config.toml`

## Photos
Stored like: `<config.storage.albums>/<album_name>/<photo_file>`

## Installation
simply:
```shell
pip install -r requirements.txt
```
or verbosely using python:
```shell
python -m pip install -r requirements.txt
```

## Running
simply:
```shell
FLASK_APP=main flask run
```
or verbosely using python:
```shell
FLASK_APP=main python -m flask run
```