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
    return send_file(sys.path[0] + '/src/telegram/{}.png'.format(slag), mimetype='image/jpeg')


@app.route('/get-BTCUSDT/<slag>/<slag2>')
def BTC_USDT(slag, slag2):
    return send_file(sys.path[0] + '/35.png', mimetype='image/jpeg')


def run_bot():
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)


def run_app():
    app.run()


if __name__ == "__main__":
    main_loop()
