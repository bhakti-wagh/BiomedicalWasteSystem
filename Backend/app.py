from flask import Flask, jsonify, request

from datetime import date, datetime
from db import get_db_connection
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


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

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT user_id, name, email, password_hash, role, is_active
        FROM users
        WHERE email = %s
    """, (email,))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    if not user["is_active"]:
        return jsonify({
            "message": "User account is inactive"
        }), 403

    if user["password_hash"] != password:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200


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
    record_date = date.today()
    record_time = datetime.now().time()

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
        (category_id, location_id, created_by, waste_type, quantity, record_date, record_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        category_id,
        location_id,
        created_by,
        waste_type,
        quantity,
        record_date,
        record_time
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





@app.route("/api/assign-bin", methods=["POST"])
def assign_bin():

    data = request.get_json()

    location_id = data.get("location_id")
    category_id = data.get("category_id")
    quantity = data.get("quantity")

    if not location_id or not category_id or not quantity:
        return jsonify({
            "message": "Location, category and quantity are required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT *
        FROM bins
        WHERE location_id = %s
        AND category_id = %s
        AND current_level + %s <= max_capacity
        AND status = 'AVAILABLE'
        LIMIT 1
    """

    cursor.execute(
        query,
        (location_id, category_id, quantity)
    )

    bin_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if not bin_data:
        return jsonify({
            "message": "No suitable bin available"
        }), 404

    return jsonify({
        "message": "Suitable bin found",
        "bin_id": bin_data["bin_id"],
        "available_space": float(
            bin_data["max_capacity"] - bin_data["current_level"]
        )
    }), 200




@app.route("/api/update-bin-level", methods=["POST"])
def update_bin_level():

    data = request.get_json()

    bin_id = data.get("bin_id")
    quantity = data.get("quantity")

    if not bin_id or not quantity:
        return jsonify({
            "message": "Bin ID and quantity are required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get current bin information
    cursor.execute("""
        SELECT *
        FROM bins
        WHERE bin_id = %s
    """, (bin_id,))

    bin_data = cursor.fetchone()

    if not bin_data:
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Bin not found"
        }), 404

    new_level = float(bin_data["current_level"]) + float(quantity)

    # Check capacity
    if new_level > float(bin_data["max_capacity"]):
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Bin capacity exceeded"
        }), 400

    # Update bin level
    cursor.execute("""
        UPDATE bins
        SET current_level = %s,
            last_updated = CURRENT_TIMESTAMP
        WHERE bin_id = %s
    """, (new_level, bin_id))

    connection.commit()


    # Check if bin is nearly full
    capacity_percentage = (new_level / float(bin_data["max_capacity"])) * 100

    if capacity_percentage >= 80:
        # Check if an open alert already exists
        cursor.execute("""
            SELECT alert_id
            FROM alerts
            WHERE bin_id = %s
            AND alert_type = 'BIN_NEAR_FULL'
            AND status = 'OPEN'
            LIMIT 1
        """, (bin_id,))

        existing_alert = cursor.fetchone()

        # Create alert only if no open alert exists
        if not existing_alert:
            cursor.execute("""
                INSERT INTO alerts
                (bin_id, alert_type, message, severity)
                VALUES (%s, %s, %s, %s)
            """, (
                bin_id,
                "BIN_NEAR_FULL",
                f"Bin {bin_id} is {capacity_percentage:.1f}% full",
                "HIGH"
            ))

            connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Bin level updated successfully",
        "bin_id": bin_id,
        "previous_level": float(bin_data["current_level"]),
        "new_level": new_level
    }), 200




@app.route("/api/bin-history", methods=["POST"])
def create_bin_history():

    data = request.get_json()

    bin_id = data.get("bin_id")
    changed_by = data.get("changed_by")
    previous_level = data.get("previous_level")
    new_level = data.get("new_level")

    if not bin_id or not changed_by:
        return jsonify({
            "message": "Bin ID and user are required"
        }), 400

    if previous_level is None or new_level is None:
        return jsonify({
            "message": "Previous level and new level are required"
        }), 400

    change_quantity = float(new_level) - float(previous_level)

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO bin_status_history
        (bin_id, changed_by, previous_level, new_level, change_quantity)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        bin_id,
        changed_by,
        previous_level,
        new_level,
        change_quantity
    )

    cursor.execute(query, values)

    connection.commit()

    history_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Bin status history created successfully",
        "history_id": history_id
    }), 201



@app.route("/api/collections", methods=["POST"])
def create_collection():

    data = request.get_json()

    waste_record_id = data.get("waste_record_id")
    bin_id = data.get("bin_id")
    collected_by = data.get("collected_by")
    quantity_collected = data.get("quantity_collected")

    collection_date = date.today()
    collection_time = datetime.now().time()

    if not waste_record_id or not bin_id or not collected_by:
        return jsonify({
            "message": "Waste record, bin and operator are required"
        }), 400

    if not quantity_collected:
        return jsonify({
            "message": "Quantity collected is required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # 1. Check the bin
    cursor.execute("""
        SELECT *
        FROM bins
        WHERE bin_id = %s
    """, (bin_id,))

    bin_data = cursor.fetchone()

    if not bin_data:
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Bin not found"
        }), 404

    # 2. Check that collection quantity is not greater than bin level
    if float(quantity_collected) > float(bin_data["current_level"]):
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Collected quantity cannot be greater than current bin level"
        }), 400

    previous_level = float(bin_data["current_level"])
    new_level = previous_level - float(quantity_collected)

    # 3. Create collection record
    query = """
        INSERT INTO collections
        (waste_record_id, bin_id, collected_by, quantity_collected,
        collection_date, collection_time, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
    waste_record_id,
    bin_id,
    collected_by,
    quantity_collected,
    collection_date,
    collection_time,
    "COMPLETED"
)
    cursor.execute(query, values)

    collection_id = cursor.lastrowid

    # 4. Update bin level
    cursor.execute("""
        UPDATE bins
        SET current_level = %s,
            last_updated = CURRENT_TIMESTAMP
        WHERE bin_id = %s
    """, (new_level, bin_id))

    # 5. Create bin status history
    change_quantity = new_level - previous_level

    cursor.execute("""
        INSERT INTO bin_status_history
        (bin_id, changed_by, previous_level, new_level, change_quantity)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        bin_id,
        collected_by,
        previous_level,
        new_level,
        change_quantity
    ))

    # 6. Check whether the bin is still near full
    capacity_percentage = (
        new_level / float(bin_data["max_capacity"])
    ) * 100

    # 7. If below 80%, resolve the open near-full alert
    if capacity_percentage < 80:

        cursor.execute("""
            UPDATE alerts
            SET status = 'RESOLVED'
            WHERE bin_id = %s
            AND alert_type = 'BIN_NEAR_FULL'
            AND status = 'OPEN'
        """, (bin_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Collection completed successfully",
        "collection_id": collection_id,
        "bin_id": bin_id,
        "previous_level": previous_level,
        "new_level": new_level
    }), 201

@app.route("/api/alerts", methods=["POST"])
def create_alert():

    data = request.get_json()

    bin_id = data.get("bin_id")
    alert_type = data.get("alert_type")
    message = data.get("message")
    severity = data.get("severity", "MEDIUM")

    if not bin_id or not alert_type or not message:
        return jsonify({
            "message": "Bin, alert type and message are required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO alerts
        (bin_id, alert_type, message, severity)
        VALUES (%s, %s, %s, %s)
    """

    values = (
        bin_id,
        alert_type,
        message,
        severity
    )

    cursor.execute(query, values)

    connection.commit()

    alert_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Alert created successfully",
        "alert_id": alert_id
    }), 201






@app.route("/api/alerts/<int:alert_id>", methods=["PUT"])
def update_alert_status(alert_id):

    data = request.get_json()

    status = data.get("status")

    if not status:
        return jsonify({
            "message": "Status is required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT alert_id
        FROM alerts
        WHERE alert_id = %s
    """, (alert_id,))

    alert = cursor.fetchone()

    if not alert:
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Alert not found"
        }), 404

    cursor.execute("""
        UPDATE alerts
        SET status = %s
        WHERE alert_id = %s
    """, (status, alert_id))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Alert status updated successfully",
        "alert_id": alert_id,
        "status": status
    }), 200





@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Total waste quantity
    cursor.execute("""
        SELECT COALESCE(SUM(quantity), 0) AS total_waste
        FROM waste_records
    """)
    total_waste = cursor.fetchone()["total_waste"]

    # Total bins
    cursor.execute("""
        SELECT COUNT(*) AS total_bins
        FROM bins
    """)
    total_bins = cursor.fetchone()["total_bins"]

    # Near-full bins
    cursor.execute("""
        SELECT COUNT(*) AS near_full_bins
        FROM bins
        WHERE current_level >= (max_capacity * 0.80)
    """)
    near_full_bins = cursor.fetchone()["near_full_bins"]

    # Open alerts
    cursor.execute("""
        SELECT COUNT(*) AS open_alerts
        FROM alerts
        WHERE status = 'OPEN'
    """)
    open_alerts = cursor.fetchone()["open_alerts"]

    # Total collections
    cursor.execute("""
        SELECT COUNT(*) AS total_collections
        FROM collections
    """)
    total_collections = cursor.fetchone()["total_collections"]

    cursor.close()
    connection.close()

    return jsonify({
        "total_waste": float(total_waste),
        "total_bins": total_bins,
        "near_full_bins": near_full_bins,
        "open_alerts": open_alerts,
        "total_collections": total_collections
    }), 200

if __name__ == "__main__":
    app.run(debug=True)