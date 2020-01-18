# import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import pandas as pd
import numpy as np

app = Flask(__name__)

# create engine
engine = create_engine("sqlite:../Resources/hawaii.sqlite")

# link database and tables
Base = automap_base()
Base.prepare(engine, reflect = True)
Base.classes.keys()

# table references
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# set homepage
@app.route("/")
def homepage():
    """List all routes that are available"""
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitaton")
def precipitation():
    
    # query
    precip_scores = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
    filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.date(2016, 8, 23)).order_by(Measurement.date).all()
    
    return jsonify(precip_scores)

@app.route("/api/v1.0/stations")
def stations():
    # query stations
    active_stations = (session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station)
                        .order_by(func.count(Measurement.station).desc())
                        .all())
   
    return jsonify(active_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year."""
    # make query
    temp_observs = (session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).all())

    return jsonify(temp_observs)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""

print(f"Lowest Temperature: {summary_temps[0][0]} Fahrenheit")
print(f"Highest Temperature: {summary_temps[0][1]} Fahrenheit")
print(f"Average Temperature: {round(summary_temps[0][2], 2)} Fahrenheit")

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
 
 last12_temps = (session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date)
                   .filter(Measurement.date >= year_ago)
                   .filter(Measurement.station == top_station)
                   .all())
temps_sum = pd.DataFrame(last12_temps)
temps_sum = temps_sum.set_index("date").sort_index(ascending=True)


if __name__ == "__main__":
    app.run(debug = True)
