# Import the dependencies.

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, desc, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
end_date = session.query(Measurement.date).order_by(desc(Measurement.date)).first()
end_date = end_date[0]
end_date = dt.datetime.strptime(end_date, "%Y-%m-%d").date()
start_date = end_date - dt.timedelta(days=365)
#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
#Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. 



@app.route("/")
def welcome():

    """List all available api routes."""
    return (
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/2010-01-01<br/>"
    f"/api/v1.0/2010-01-01/2017-08-23"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return 12 months of precipitation data from the most recent date in the dataset"""
    # Query the last 12 months of precipitation data
    
    results = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).all()
    
    session.close()
    
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    
    """Return a JSON list of stations from the dataset."""
    # Query the list of stations
    query = session.query(Station.station).all()

    session.close()

    results = [i.station for i in query]
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    
    """Return a JSON list of temperature observations for the previous year."""
    # Query the dates and temperature observations of the most-active station for the previous year of data
    active_stations = session.query(Measurement.station,func.count(Measurement.prcp)).group_by(Measurement.station).order_by(desc(func.count(Measurement.prcp))).all()
    most_active_station = active_stations[0][0]
    
    query = session.query(Measurement.tobs).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).filter(Measurement.station == most_active_station).all()
    
    session.close()
    
    results = [i.tobs for i in query]
    return jsonify(results)

#/api/v1.0/<start> and /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>")
def start(start):
    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
       
    query = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    results = [round(i,2) for i in query[0]]
    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
       
    query = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    results = [round(i,2) for i in query[0]]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)