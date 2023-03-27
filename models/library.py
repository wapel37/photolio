import os.path

from .album import Album


class Library:
    def __init__(self, path: str):
        self.path = path

    @property
    def albums(self) -> list[Album]:
        return sorted(
            [Album(os.path.join(self.path, name)) for name in os.listdir(self.path)],
            key=lambda a: a.name.lower()
        ) if os.path.exists(self.path) else []

    def __iter__(self):
        return iter(self.albums)

    def __getitem__(self, item: str) -> Album:
        path = os.path.join(self.path, item)
        if not os.path.exists(path):
            raise KeyError()
        return Album(path)
