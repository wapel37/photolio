import os.path
import exif

from .thumbnail import Thumbnail


class Photo:
    to_url = lambda _: None

    def __init__(self, album: object, path: str):
        self.path = path
        self.name = os.path.basename(path)
        self.album = album

    @property
    def info(self) -> str:
        image = exif.Image(self.path)
        exif_data = image.get_all()

        photo_params = [
            ('photographic_sensitivity', 'ISO {v}'),
            ('f_number', 'F/{v}'),
            ('exposure_time', '1/{1/v:.0f}s'),
            ('focal_length', '{v:.0f}mm'),
        ]
        camera_params = [
            ('lens_model', '{v}'),
            ('model', '{v}'),
        ]

        # not best, coz `eval` but works :)
        photo_info = [eval(f'f"{pattern}"', {'v': exif_data[param]}) for param, pattern in photo_params if
                      param in exif_data]
        camera_info = [eval(f'f"{pattern}"', {'v': exif_data[param]}) for param, pattern in camera_params if
                       param in exif_data]
        return '\n'.join([' '.join(photo_info), *camera_info])

    def __str__(self):
        return self.name

    @property
    def url(self) -> str | None:
        return Photo.to_url(self)

    @property
    def thumbnail(self) -> Thumbnail:
        return Thumbnail(self)
