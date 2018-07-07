#coding:utf8

from app import app
from gevent.pywsgi import WSGIServer


if __name__ == "__main__":
    # WSGIServer(('0.0.0.0',5003),app).serve_forever()
    app.run(
        host='0.0.0.0',
        port=5003,
        debug=True
    )