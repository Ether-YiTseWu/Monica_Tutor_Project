import flask
from flask_bootstrap import Bootstrap

app = flask.Flask(__name__)
Bootstrap(app)

@app.route("/")
def indexHTML():
    return flask.render_template('index.html')

@app.route("/find")
def example():
    return "OK"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080, debug = True)