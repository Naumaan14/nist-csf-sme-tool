from flask import Flask
app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)
