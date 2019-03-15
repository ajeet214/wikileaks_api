from flask import Flask, jsonify, request
from modules.wikileaks import Wikileaks
from raven.contrib.flask import Sentry

app = Flask(__name__)
sentry = Sentry(app)


@app.route('/api/v1/search')
def search():
    query = request.args.get('q')
    obj = Wikileaks()
    return jsonify(obj.wikileaks(query))


if __name__ == '__main__':
    app.run(port=5010)
