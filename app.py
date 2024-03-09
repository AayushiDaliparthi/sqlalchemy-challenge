# Import dependencies
import datetime as dt
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Database setup
database_path = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)

# Define routes
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_date = session.query(func.max(Measurement.date)).scalar()
    cutoff_date = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= cutoff_date).all()
    session.close()

    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()
    session.close()

    station_data = [{"station": station, "name": name} for station, name in results]
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date = session.query(func.max(Measurement.date)).scalar()
    cutoff_date = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= cutoff_date).all()
    session.close()

    tobs_data = {date: tobs for date, tobs in results}
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temps_start(start):
    session = Session(engine)
    results = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    temp_data = {
        "average_temperature": results[0][0],
        "min_temperature": results[0][1],
        "max_temperature": results[0][2]
    }
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start, end):
    session = Session(engine)
    results = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    temp_data = {
        "average_temperature": results[0][0],
        "min_temperature": results[0][1],
        "max_temperature": results[0][2]
    }
    return jsonify(temp_data)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
