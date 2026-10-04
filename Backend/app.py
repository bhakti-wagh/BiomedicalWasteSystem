from flask import Flask, jsonify,request
from db import get_db_connection

app = Flask(__name__)


@app.route("/")
def home():
    return "Biomedical Waste Management System Backend is Running!"


@app.route("/test-db")
def test_db():
    connection = get_db_connection()

    if connection.is_connected():
        connection.close()
        return "Database Connected Successfully!"

    return "Database Connection Failed!"



@app.route("/api/locations")
def get_locations():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM locations")

    locations = cursor.fetchall()

    cursor.close()
    connection.close()

    return locations



@app.route("/api/categories")
def get_categories():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categories")

    categories = cursor.fetchall()

    cursor.close()
    connection.close()

    return categories

@app.route("/api/bins")
def get_bins():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM bins")

    bins = cursor.fetchall()

    cursor.close()
    connection.close()

    return bins


@app.route("/api/waste-records")
def get_waste_records():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM waste_records")

    waste_records = cursor.fetchall()

    for record in waste_records:
        if record["record_date"]:
            record["record_date"] = str(record["record_date"])

        if record["record_time"]:
            record["record_time"] = str(record["record_time"])

    cursor.close()
    connection.close()

    return jsonify(waste_records)


@app.route("/api/collections")
def get_collections():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM collections")

    collections = cursor.fetchall()

    for collection in collections:
        if collection["collection_date"]:
            collection["collection_date"] = str(collection["collection_date"])

        if collection["collection_time"]:
            collection["collection_time"] = str(collection["collection_time"])

    cursor.close()
    connection.close()

    return jsonify(collections)



@app.route("/api/alerts")
def get_alerts():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM alerts")

    alerts = cursor.fetchall()

    for alert in alerts:
        if alert["created_at"]:
            alert["created_at"] = str(alert["created_at"])

    cursor.close()
    connection.close()

    return jsonify(alerts)

@app.route("/api/users")
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT user_id, name, email, role, phone, is_active, created_at
        FROM users
    """)

    users = cursor.fetchall()

    for user in users:
        if user["created_at"]:
            user["created_at"] = str(user["created_at"])

    cursor.close()
    connection.close()

    return jsonify(users)




@app.route("/api/waste-records", methods=["POST"])
def create_waste_record():

    data = request.get_json()

    category_id = data.get("category_id")
    location_id = data.get("location_id")
    created_by = data.get("created_by")
    waste_type = data.get("waste_type")
    quantity = data.get("quantity")

    if not category_id or not location_id or not created_by:
        return jsonify({
            "message": "Category, location and user are required"
        }), 400

    if not waste_type or not quantity:
        return jsonify({
            "message": "Waste type and quantity are required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO waste_records
        (category_id, location_id, created_by, waste_type, quantity)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        category_id,
        location_id,
        created_by,
        waste_type,
        quantity
    )

    cursor.execute(query, values)

    connection.commit()

    waste_record_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Waste record created successfully",
        "waste_record_id": waste_record_id
    }), 201

if __name__ == "__main__":
    app.run(debug=True)