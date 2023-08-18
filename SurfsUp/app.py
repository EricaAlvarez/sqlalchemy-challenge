# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/stations:<br/>"
        f"/api/v1.0/tobs:<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the last 12 months"""
    # Query all passangers
    last_months = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    last_year = dt.datetime.strptime(last_months, '%Y-%m-%d') - dt.timedelta(days=365)
    print(last_year)

    rain = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_year).\
    order_by(Measurement.date).all()

    prcp_df = pd.DataFrame(rain, columns=['Date', 'Precipitation'])
    prcp_df.set_index('Date', inplace=True)
    prcp_df = prcp_df.dropna()

    session.close()

    # Create a dictionary from the row data and append to a list of last year data
    last_year_data = []
    for date, precipitation, sex in prcp_df:
        year_dict = {}
        year_dict["Date"] = date
        year_dict["Precipitation"] = precipitation
        last_year_data.append(last_year_data)

    return jsonify(last_year_data)


if __name__ == '__main__':
    app.run(debug=True)
