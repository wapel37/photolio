import os

from .photo import Photo


extensions = {'jpg', 'jpeg', 'png'}
public_filename = '.public'


class Album:
    to_url = lambda _: None

    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(path)

    @property
    def public(self) -> bool:
        return os.path.exists(os.path.join(self.path, public_filename))

    @public.setter
    def public(self, value: bool):
        if value == self.public:
            return
        public_filepath = os.path.join(self.path, public_filename)
        if value:
            open(public_filepath, 'w+').close()
        else:
            os.remove(public_filepath)

    @property
    def photos(self) -> list[Photo]:
        return sorted([
            Photo(self, os.path.join(self.path, filename))
            for filename
            in os.listdir(self.path)
            if filename.split('.')[-1].lower() in extensions
        ], key=lambda p: p.name)

    @property
    def enumerated(self):
        return enumerate(self)

    def __iter__(self):
        return iter(self.photos)

    def __getitem__(self, item: int | str) -> Photo:
        if item is int:
            return self.photos[item]
        path = os.path.join(self.path, item)
        if not os.path.exists(path):
            raise KeyError()
        return Photo(self, path)

    def __str__(self):
        return self.name

    @property
    def url(self) -> str | None:
        return Album.to_url(self)

    @property
    def thumbnail(self) -> Photo | None:
        if len(self.photos) > 0:
            return self.photos[0]
        return None
