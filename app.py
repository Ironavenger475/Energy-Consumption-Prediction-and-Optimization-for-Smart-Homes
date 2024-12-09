from flask import Flask, jsonify, send_from_directory, request
import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Azure SQL Database connection string
db_connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=tcp:chittitu.database.windows.net,1433;"
    "Database=chittitu_ssms;"
    "Uid=chittitu;"
    "Pwd=tulasi_2001;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Route to serve index.html
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

# Endpoint to fetch data for display
@app.route('/data', methods=['GET'])
def get_data():
    try:
        home_id = request.args.get('home_id')
        # Set up the connection to the database
        conn = pyodbc.connect(db_connection_string)
        cursor = conn.cursor()
        
        # Execute query to fetch data
        query = '''
            SELECT home_id, appliance, energy_consumption_kWh, usage_duration_minutes
            FROM EnergyUsage
            WHERE home_id = ?
            ORDER BY energy_consumption_kWh DESC
        '''
        cursor.execute(query, (home_id,))
        rows = cursor.fetchall()
        
        # Format the result into a list of dictionaries
        result = [
            {'home_id': row[0], 'appliance': row[1], 'energy_consumption_kWh': row[2], 'usage_duration_minutes': row[3]}
            for row in rows
        ]
        
        cursor.close()
        conn.close()
        
        return jsonify(result)
    
    except Exception as e:
        print('Error fetching data:', e)
        return 'Error fetching data', 500

# Route to serve display.html
@app.route('/display')
def display():
    return send_from_directory(os.getcwd(), 'display.html')

# Start the server with the updated code
if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 3000)))