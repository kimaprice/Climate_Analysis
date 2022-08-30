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
from sqlalchemy import create_engine, func, inspect

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

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
    return(

        
    )

@app.route("/api/v1.0/<start>")
def startdate():
    return(

        
    )

@app.route("/api/v1.0/<start>/<end>")
def enddate():
    return(

        
    )


if __name__ == '__main__':
    app.run(debug=True)

