#Import libraries
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc

from flask import Flask, jsonify

#######Connect to DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measure = Base.classes.measurement
station = Base.classes.station

#set up Flask
app = Flask(__name__)

###############routes###############

#Home
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stats/<start>/<end><br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365) 

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(measure.date, measure.prcp).filter(measure.date >= year_ago).all()

    session.close()

    precip_dict = {}
    
    for date, prcp in results:
        precip_dict.update({date : prcp})

    return(
        jsonify(precip_dict)
    )

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Get the list of stations
    results = session.query(station.name).all()

    session.close()

    all_names = list(np.ravel(results))

    return(
        jsonify(all_names)
    )
    
@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Find most Active weather station
    active_stations = session.query(measure.station, station.name, func.count(measure.id).label('num_records')).filter(measure.station == station.station).group_by(measure.station).order_by(desc('num_records')).all()
    most_active = active_stations[0][0]

    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365) 

    #Get data for last year temps for most active station
    results = session.query(measure.date, measure.tobs).filter(measure.date >= year_ago).filter(measure.station == most_active).all()

    session.close()

    #Creat a list of dictionaires for date and temperatures
    station_temps = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict[date] = tobs
        station_temps.append(temp_dict)

    return(
        jsonify(station_temps)
    )

@app.route("/api/v1.0/stats/<start_date>/<end_date>")
@app.route("/api/v1.0/stats/<start_date>")
def stats_start_date(start_date, end_date ="no_end"):
   
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Get the max, min, avg temps for the date range
    sel = [func.max(measure.tobs).label('max_temp'), func.min(measure.tobs).label('min_temp'), func.avg(measure.tobs).label('avg_temp')]
    if end_date == "no_end":
        stats = session.query(*sel).filter(measure.date >= start_date).all()
    else:
        stats = session.query(*sel).filter(measure.date >= start_date).filter(measure.date <= end_date).all()

    session.close()

    #Create dictionary for results
    temp_dict = {}
    temp_dict["start_date"] = start_date
    temp_dict["end_date"] = end_date
    temp_dict["max_temp"] = stats[0][0]
    temp_dict["min_temp"] = stats[0][1]
    temp_dict["avg_temp"] = stats[0][2]

    return(
        jsonify(temp_dict) 
    )


if __name__ == '__main__':
    app.run(debug=True)

