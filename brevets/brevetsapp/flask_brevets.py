"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import os
import flask
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import json
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import logging
import config
CONFIG = config.configuration()

###
# Globals
###
app = flask.Flask(__name__)
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb
###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!
    
    brev_dist = request.args.get('brev_dist', type=float)
    start_time = request.args.get('start_time', type=str)
    # Needed to get our input time from str to arrow object.
    arrow_start = arrow.get(start_time, "YYYY-MM-DDTHH:mm")
    open_time = acp_times.open_time(km, brev_dist, arrow_start).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brev_dist, arrow_start).format('YYYY-MM-DDTHH:mm')
    app.logger.debug("close time={}".format(close_time))
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/someroute", methods=['POST'])
def someroute():
    brevet_input = json.loads(request.form.get("brevet_data", type=str))
    db.tododb.drop()
    for index in brevet_input:
        item_doc = {
            'kms': index['kms'],
            'open': index['open'],
            'close': index['close']
        }
        db.tododb.insert_one(item_doc)
    app.logger.debug("brevet_data: " + str(brevet_input))
    return redirect(url_for('index'))

@app.route("/displayroute")
def dispaly():
    return flask.render_template('displayroute.html', items=list(db.tododb.find()))

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
