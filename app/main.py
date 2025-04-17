import os
import psycopg2
from flask import Flask

# Create the Flask app
app = Flask(__name__)

# Create the index route
@app.route("/")
def index():
    return "The API is working"

# Create a general DB to GeoJSON function
def database_to_geojson(table_name):
    # Create a connection to the database
    conn = psycopg2.connect(
        host = os.environ.get("DB_HOST"),
        database = os.environ.get("DB_NAME"),
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASS"),
        port = os.environ.get("DB_PORT")
    )

    # Execute a query to retrieve the data
    with conn.cursor() as cur:
        query = f"""
        SELECT JSON_BUILD_OBJECT(
            'type', 'FeatureCollection',
            'features', JSON_AGG(
                ST_AsGeoJSON({table_name}.*)::json
            )
        )
        FROM {table_name}
        """

        cur.execute(query)

        data = cur.fetchall()

    # Close the connection
    conn.close()

    # Returning the data
    return data[0][0]


# Create the data route
@app.route("/elevations", methods=["GET"])
def elevations():
    return database_to_geojson("interpolated_elevation")

# Create the data route
@app.route("/temperature", methods=["GET"])
def temperature():
    return database_to_geojson("interpolated_temp")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))