import io
import os.path

import hashlib

import PIL.Image
import PIL.ImageOps

import config

os.makedirs(os.path.abspath(config.storage['cache']), exist_ok=True)


class Thumbnail:
    to_url = lambda _: None

    def __init__(self, photo: object, size: int = 512):
        self.photo = photo
        self.original_path = getattr(photo, 'path')
        self.size = size

    def thumbnail(self) -> bytes:
        image = PIL.Image.open(self.original_path)
        image_format = image.format

        image = PIL.ImageOps.exif_transpose(image)
        image.thumbnail((self.size, self.size), resample=PIL.Image.ANTIALIAS)

        stream = io.BytesIO()
        image.save(stream, format=image_format, quality=90)
        stream.seek(0)
        return stream.read()

    @property
    def path(self) -> str:
        *_, extension = self.original_path.split('.')
        with open(self.original_path, 'rb') as file:
            filehash = hashlib.sha256(file.read()).hexdigest()
        filename = f'{filehash}.{self.size}.{extension}'
        thumbnail_filepath = os.path.join(config.storage['cache'], filename)

        if not os.path.exists(thumbnail_filepath):
            with open(thumbnail_filepath, 'wb+') as file:
                file.write(self.thumbnail())

        return thumbnail_filepath

    @property
    def url(self) -> str | None:
        return Thumbnail.to_url(self)
