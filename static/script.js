const ROUTES = [
    "Hyderabad → Bangalore", "Hyderabad → Chennai", "Hyderabad → Mumbai", "Hyderabad → Delhi",
    "Bangalore → Chennai", "Bangalore → Mumbai", "Mumbai → Delhi", "Chennai → Kolkata",
    "Delhi → Jaipur", "Pune → Goa"
];

const BUS_TYPES = [
    { type: "AC Sleeper", fare: 850 },
    { type: "Non-AC Sleeper", fare: 550 },
    { type: "AC Seater", fare: 650 },
    { type: "Non-AC Seater", fare: 400 },
    { type: "Volvo Multi-Axle", fare: 1200 }
];

document.addEventListener('DOMContentLoaded', () => {
    const routeSelect = document.getElementById('route');
    const busTypeSelect = document.getElementById('busType');
    const dateSelect = document.getElementById('date');
    const fareTotal = document.getElementById('fareTotal');
    const bookingForm = document.getElementById('bookingForm');
    const successModal = document.getElementById('successModal');
    const ticketDetails = document.getElementById('ticketDetails');

    // Populate Routes
    ROUTES.forEach(route => {
        const option = document.createElement('option');
        option.value = route;
        option.textContent = route;
        routeSelect.appendChild(option);
    });

    // Populate Bus Types
    BUS_TYPES.forEach(bus => {
        const option = document.createElement('option');
        option.value = bus.type;
        option.textContent = `${bus.type} (₹${bus.fare})`;
        busTypeSelect.appendChild(option);
    });

    // Populate Dates (Next 30 days)
    for (let i = 1; i <= 30; i++) {
        const date = new Date();
        date.setDate(date.getDate() + i);
        const dateStr = date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }).replace(/ /g, '-');
        const option = document.createElement('option');
        option.value = dateStr;
        option.textContent = dateStr;
        dateSelect.appendChild(option);
    }

    // Fare Calculation
    const updateFare = () => {
        const selectedBus = BUS_TYPES.find(b => b.type === busTypeSelect.value);
        const seats = parseInt(document.getElementById('seats').value) || 0;
        const total = selectedBus ? selectedBus.fare * seats : 0;
        fareTotal.textContent = `₹${total}`;
        return total;
    };

    busTypeSelect.addEventListener('change', updateFare);
    document.getElementById('seats').addEventListener('input', updateFare);
    updateFare();

    // Form Submission
    bookingForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const ticketId = 'TKT-' + Math.random().toString(36).substr(2, 8).toUpperCase();
        const total = updateFare();
        
        const details = {
            "Ticket ID": ticketId,
            "Passenger": document.getElementById('name').value,
            "Age": document.getElementById('age').value,
            "Route": routeSelect.value,
            "Date": dateSelect.value,
            "Bus": busTypeSelect.value,
            "Seats": document.getElementById('seats').value,
            "Total Fare": `₹${total}`
        };

        // --- SEND TO BACKEND (Flask) ---
        fetch('/book', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(details)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Server response:", data);
            
            // Show Success Modal
            ticketDetails.innerHTML = Object.entries(details).map(([label, val]) => `
                <div class="ticket-row">
                    <span class="label">${label}</span>
                    <span class="val">${val}</span>
                </div>
            `).join('');

            successModal.style.display = 'grid';
        });
    });

    // Reset handler
    bookingForm.addEventListener('reset', () => {
        setTimeout(updateFare, 0);
    });
});

function closeModal() {
    document.getElementById('successModal').style.display = 'none';
}
