import datetime
import time

import analytics
import get_clean_data
import powerdash_info
import redis
from flask import Flask, request, jsonify

import matplotlib.pyplot as plt
import io
import base64


app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, world!'

@app.route('/')
def build_plot():

    img = io.BytesIO()

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]
    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.debug=True
    app.run(host='127.0.0.1', port=port)