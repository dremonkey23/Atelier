from .bot import run
from .settings import load_settings


if __name__ == "__main__":
    run(load_settings())
