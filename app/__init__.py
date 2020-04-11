from flask import Flask

webapp = Flask(__name__)

from app import main
from app import config
from app import utils

if __name__ == '__main__':
    webapp.run()