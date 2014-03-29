import argparse

from flask import Flask, render_template
from rapid_response_kit.utils.registry import Registry
from rapid_response_kit.tools import autorespond
from rapid_response_kit.tools import broadcast
from rapid_response_kit.tools import conference_line
from rapid_response_kit.tools import forward
from rapid_response_kit.tools import ringdown
from rapid_response_kit.tools import simplehelp
from rapid_response_kit.tools import survey
from rapid_response_kit.tools import town_hall
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config.from_object('rapid_response_kit.utils.config')

app.config.apps = Registry()

app.config['NUMBERSDB'] = 'db/phone_numbers.json'

autorespond.install(app)
broadcast.install(app)
conference_line.install(app)
forward.install(app)
ringdown.install(app)
simplehelp.install(app)
survey.install(app)
town_hall.install(app)

@auth.get_password
def get_pw(username):
    if username == app.config['USER']:
        return app.config['PASSWORD']
    return None

@app.route('/')
@auth.login_required
def home():
    return render_template('home.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=5000, action="store",
                        help="The port to run the Twilio Toolkit on")
    parser.add_argument('--debug', default=False, action="store_true",
                        help="Turn on debug mode")
    args = parser.parse_args()
    app.run(debug=args.debug, port=int(args.port))
