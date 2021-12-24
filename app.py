# set up the flask weather app

import datetime as dt
#import numpy as np
#import pandas as pd

# now lets get the dependencies we need for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import flask
from flask import Flask, jsonify # this is always like this

# Set up the Database

# the code on bottom will access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes
# Base.prepare() will be used to reflect the tables
Base = automap_base()
Base.prepare(engine, reflect = True)

# then we can save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# finallym create a session link from Python to our database with the following code
session = Session(engine)

# Set Up Flask

# create a flask application called app
app = Flask(__name__) # always like this

########################################
# CREATE THE WELCOME ROUTE

# we want our welcome route to be the root
@app.route("/") # alwasy like this

# create a function welcome() with a retrun statement
# add the precipitaion, stations, tobs and temp routes that we need for this module into our return statement
# we use f-strings to displat them for our investors
# when creating routes, we name the convention /api/v1.0/ followed by the name of the route.  it signifies that this is version 1 of our application. it can be updated to support future versions of the app as well
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

##############################
# PRECIPITATION ROUTE

@app.route("/api/v1.0/precipitation")

# next we will create the precipitation() function
def precipitaion():
    # first we want to add the line of code that calculates the date one year ago from the most recent date in the database.
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # next we write a query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    
    # we will use jsonify() to format our results into a JSON structured file
    precip = {date:prcp for date, prcp in precipitation}
    
    return jsonify(precip)
# http://127.0.0.1:5000/api/v1.0/precipitation
# add api/v1.0/precipitation at the end of the URL to see the precipitaion route

###############################
# STATIONS ROUTE

@app.route("/api/v1.0/stations")

def stations():
    # we need to create a query that will allow us to get all of the stations in our database
    results = session.query(Station.station).all()
    
    # we want to start by unraveling(解开） our results into a one dimensional array
    # we want to use the function np.ravel() with results as our parameter
    # next we will convert our unraveled results into a list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# http://127.0.0.1:5000/api/v1.0/stations

################################
#MONTHLY TEMPERATURE ROUTE

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# http://127.0.0.1:5000/api/v1.0/tobs

########################################
# STATISTICS ROUTE

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# add the start and end parameters.
def stats(start=None, end=None):
    # create a query to select the minimum, average and maximum temps from SQLite database
    # create a list call sel
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # since we need to determine the starting and ending datem use if-not statement
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# if you want to check the min max and avg temps for june 2017, use the following link
# http://127.0.0.1:5000/api/v1.0/temp/2017-06-01/2017-06-30









