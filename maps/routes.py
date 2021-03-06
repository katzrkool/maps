"""
Define routes.
"""
from datetime import datetime, timedelta
import pytz
from flask import render_template, jsonify
from maps import app
from maps.models import Call
from maps.util import convert_naive_to_db


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch/<days>')
def fetch_days(days=1):
    days = float(days)

    # Get current date
    now = datetime.now(tz=app.config['TIMEZONE'])
    start = now - timedelta(days=days)

    data = Call.query.filter(Call.timestamp.between(start, now)).all()

    # Convert all the call objects to dict
    return jsonify([i.serialize for i in data])


@app.route('/fetch/<start>/<end>')
def fetch_date_range(start, end):
    # Note: start and end are treated as America/Chicago time
    local_timezone = pytz.timezone("America/Chicago")

    # Start should be beginning of day
    start += 'T00:00:00'
    # End should be end of day
    end += 'T23:59:59'

    try:
        start = convert_naive_to_db(datetime.strptime(start, '%Y-%m-%dT%H:%M:%S'), local_timezone)
        end = convert_naive_to_db(datetime.strptime(end, '%Y-%m-%dT%H:%M:%S'), local_timezone)
    except ValueError:
        return 'Invalid Dates. Dates should be in YYYY-MM-DD format.', 400

    data = Call.query.filter(Call.timestamp.between(start, end)).all()

    # Convert all the call objects to dict
    return jsonify([i.serialize for i in data])
