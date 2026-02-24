from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Supriya@4321",
    database="realestate"
)
cursor = db.cursor(dictionary=True)

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Get all properties
@app.route('/properties', methods=['GET'])
def get_properties():
    status = request.args.get('status')
    query = "SELECT * FROM properties"
    params = []
    if status == 'available':
        query += " WHERE status='available'"
    elif status == 'rent':
        query += " WHERE status='rent'"
    cursor.execute(query, params)
    return jsonify(cursor.fetchall())

# Buy property
@app.route('/buy_property', methods=['POST'])
def buy_property():
    data = request.get_json()
    prop_id = data['property_id']
    name = data['client_name']
    phone = data['client_phone']
    amount = data['amount']

    cursor.execute("INSERT INTO clients (name, contact, client_type) VALUES (%s,%s,'buyer')", (name, phone))
    client_id = cursor.lastrowid

    cursor.execute("INSERT INTO transactions (property_id, client_id, transaction_type, date, amount) VALUES (%s,%s,'sale',CURDATE(),%s)", (prop_id, client_id, amount))
    cursor.execute("UPDATE properties SET status='sold' WHERE id=%s", (prop_id,))
    db.commit()
    return jsonify({"message":"Property bought successfully!"})

# Rent property
@app.route('/rent_property', methods=['POST'])
def rent_property():
    data = request.get_json()
    prop_id = data['property_id']
    name = data['client_name']
    phone = data['client_phone']
    amount = data['amount']

    cursor.execute("INSERT INTO clients (name, contact, client_type) VALUES (%s,%s,'tenant')", (name, phone))
    client_id = cursor.lastrowid

    cursor.execute("INSERT INTO transactions (property_id, client_id, transaction_type, date, amount) VALUES (%s,%s,'rent',CURDATE(),%s)", (prop_id, client_id, amount))
    cursor.execute("UPDATE properties SET status='rent' WHERE id=%s", (prop_id,))
    db.commit()
    return jsonify({"message":"Property rented successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
