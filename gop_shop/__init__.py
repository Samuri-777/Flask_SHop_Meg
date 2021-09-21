from flask import Flask

app = Flask(__name__)


from gop_shop import routes
