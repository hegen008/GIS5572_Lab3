import os
import psycopg2
from flask import Flask

# Create the Flask app
app = Flask(__name__)

# Create the index route
@app.route("/")
def index():
    return "The API is working"

# Create the data route
@app.route("/elevations", methods=["GET"])
def elevations():
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
        query = """
        SELECT JSON_BUILD_OBJECT(
            'type', 'FeatureCollection',
            'features', JSON_AGG(
                ST_AsGeoJSON(interpolated_elevation.*)::json
            )
        )
        FROM interpolated_elevation;
        """

        cur.execute(query)

        data = cur.fetchall()

    # Close the connection
    conn.close()

    # Returning the data
    return data[0][0]

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))