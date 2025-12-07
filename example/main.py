from ..src.config import Config
from ..src.controller import Controller

controller = Controller.create(Config("config.ini"))
