from src.app import app
from flask import Response
from json import dumps

@app.route('/health')
def index():
    return Response(dumps({'response':'up'}), status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run()
