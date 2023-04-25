import flask

app = flask.Flask(__name__)


@app.route('/teapot', methods=['GET'])
def teapot():
    return flask.Response("I'm a teapot 418", status=418, mimetype='text/plain')


app.run(host='0.0.0.0', port=8000)
