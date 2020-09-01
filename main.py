from src.app import app
from flask import Response
from json import dumps
from src.api.REST.routes import api
from flask import send_file
import sys
from concurrent.futures import ProcessPoolExecutor
from src.genimg import run_shedule


app.register_blueprint(api, url_prefix='/api/v1.0')
executor = ProcessPoolExecutor(max_workers=2)


@app.route('/health')
def index():
    return Response(dumps({'response': 'up'}), status=200, mimetype='application/json')


if __name__ == "__main__":
    executor.submit(run_shedule)
    app.run()
