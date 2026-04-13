from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# --- ROUTES ---
@app.route('/')
def home():
    print(f"\n[SERVER] New visitor connected from {request.remote_addr} at {datetime.now().strftime('%H:%M:%S')}")
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book_ticket():
    data = request.json
    
    # Extract data
    name = data.get('Passenger', 'N/A')
    tid = data.get('Ticket ID', 'N/A')
    route = data.get('Route', 'N/A')
    total = data.get('Total Fare', '₹0')
    
    # --- Python Logic (Printing to Terminal) ---
    sep = "=" * 50
    print(f"\n{sep}")
    print(f"   NEW BOOKING RECEIVED")
    print(sep)
    print(f"   Ticket ID      : {tid}")
    print(f"   Passenger Name : {name}")
    print(f"   Route          : {route}")
    print(f"   Total Fare     : {total}")
    print(f"   Booked At      : {datetime.now().strftime('%d-%b-%Y %I:%M %p')}")
    print(sep)
    print(f"   Booking Successful for customer: {name}\n")

    return jsonify({"status": "success", "ticket_id": tid})

if __name__ == '__main__':
    # host='0.0.0.0' allows anyone on the same network to connect via your IP
    port = int(os.environ.get('PORT', 5000))
    print(f"\n{'-'*50}")
    print(f"  Bus Booking Server Starting...")
    print(f"  Local: http://localhost:{port}")
    print(f"  Network: Check your IP address to share!")
    print(f"{'-'*50}\n")
    app.run(host='0.0.0.0', port=port, debug=True)
