from flask import Flask
from .conf.config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
