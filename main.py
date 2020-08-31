from src.app import app
from flask import Response
from json import dumps
from src.api.REST.routes import api
from src.telegram.bot import main_loop
from flask import send_file
import sys
from concurrent.futures import ProcessPoolExecutor

app.register_blueprint(api, url_prefix='/api/v1.0')
executor = ProcessPoolExecutor(max_workers=4)


@app.route('/health')
def index():
    return Response(dumps({'response': 'up'}), status=200, mimetype='application/json')


@app.route('/get-chart/<slag>/<slag2>')
def photo(slag, slag2):
    return send_file(sys.path[0] + '/src/img/{}.png'.format(slag), mimetype='image/jpeg')


@app.route('/get-BTCUSDT/<slag>')
def BTC_USDT(slag):
    return send_file(sys.path[0] + 'src/img/icon-BTC.png', mimetype='image/jpeg')


if __name__ == "__main__":
    app.run()
