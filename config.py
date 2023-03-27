import toml


config = toml.load('config.toml')


def __dir__():
    return config.keys()


def __getattr__(name):
    return config.get(name)
