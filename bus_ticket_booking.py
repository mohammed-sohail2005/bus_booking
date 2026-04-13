import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import random, string

# Colors
BG, CARD_BG, ACCENT, TEXT, TEXT_DIM, ENTRY_BG, BORDER = "#0f172a", "#1e293b", "#3b82f6", "#f8fafc", "#94a3b8", "#334155", "#475569"

class BusTicketBookingApp:
    ROUTES = ["Hyderabad → Bangalore", "Hyderabad → Chennai", "Hyderabad → Mumbai", "Hyderabad → Delhi", "Bangalore → Chennai", "Bangalore → Mumbai", "Mumbai → Delhi", "Chennai → Kolkata", "Delhi → Jaipur", "Pune → Goa"]
    BUS_TYPES = ["AC Sleeper", "Non-AC Sleeper", "AC Seater", "Non-AC Seater", "Volvo Multi-Axle"]
    SEAT_PREFS = ["Window", "Aisle", "No Preference"]

    def __init__(self, root):
        self.root = root
        self.root.title("🚌 Bus Ticket Booking")
        self.root.geometry("520x760")
        self.root.configure(bg=BG)
        self.root.resizable(0, 0)
        
        # Header
        h = tk.Frame(root, bg=ACCENT, height=80)
        h.pack(fill="x")
        tk.Label(h, text="🚌  Bus Ticket Booking", font=("Segoe UI", 20, "bold"), bg=ACCENT, fg="white").pack(pady=(10, 0))
        tk.Label(h, text="Book your journey  •  Fast & Easy", font=("Segoe UI", 10), bg=ACCENT, fg="#dbeafe").pack()

        # Form Card
        card = tk.Frame(root, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=15)
        self.inner = tk.Frame(card, bg=CARD_BG)
        self.inner.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.vars = {}
        self.widgets = {}
        self.row = 0
        
        # Fields
        self.vars["Name"] = self._add_field("Passenger Name", "entry", placeholder="Enter full name")
        self.vars["Age"] = self._add_field("Age", "spin", range=(1, 120))
        self.vars["Gender"] = self._add_field("Gender", "radio", options=["Male", "Female", "Other"])
        self.vars["Phone"] = self._add_field("Phone Number", "entry", placeholder="10-digit mobile number")
        self.vars["Route"] = self._add_field("Select Route", "combo", options=self.ROUTES)
        self.vars["Date"] = self._add_field("Travel Date", "combo", options=[(datetime.now()+timedelta(days=i)).strftime("%d-%b-%Y") for i in range(1, 31)])
        self.vars["Bus"] = self._add_field("Bus Type", "combo", options=self.BUS_TYPES)
        self.vars["Seats"] = self._add_field("Number of Seats", "spin", range=(1, 10))
        self.vars["Pref"] = self._add_field("Seat Preference", "combo", options=self.SEAT_PREFS)

        # Buttons
        btn_f = tk.Frame(root, bg=BG)
        btn_f.pack(fill="x", padx=20, pady=(0, 10))
        tk.Button(btn_f, text="🎫 Book Ticket", font=("Segoe UI", 12, "bold"), bg=ACCENT, fg="white", command=self._on_book).pack(side="left", expand=1, fill="x", padx=(0,5))
        tk.Button(btn_f, text="🔄 Reset", font=("Segoe UI", 12, "bold"), bg=ENTRY_BG, fg=TEXT, command=self._on_reset).pack(side="left", expand=1, fill="x", padx=(5,0))
        
        tk.Label(root, text="Exp-9 • GUI Programming Tools • Tkinter Demo", font=("Segoe UI", 9), bg=BG, fg=TEXT_DIM).pack(pady=(0, 10))

    def _add_field(self, lbl_txt, type, options=None, range=None, placeholder=None):
        tk.Label(self.inner, text=lbl_txt, font=("Segoe UI", 10, "bold"), bg=CARD_BG, fg=TEXT_DIM).grid(row=self.row, column=0, sticky="w")
        self.row += 1
        var = tk.StringVar(value=options[0] if options and type=="combo" else (placeholder if placeholder else ""))
        if type == "entry":
            w = tk.Entry(self.inner, textvariable=var, font=("Segoe UI", 10), bg=ENTRY_BG, fg=TEXT if not placeholder else TEXT_DIM, highlightthickness=1, highlightbackground=BORDER, relief="flat")
            w.grid(row=self.row, column=0, sticky="ew", pady=(0, 10), ipady=3)
            if placeholder:
                w.bind("<FocusIn>", lambda e: (var.set(""), w.config(fg=TEXT)) if var.get()==placeholder else None)
                w.bind("<FocusOut>", lambda e: (var.set(placeholder), w.config(fg=TEXT_DIM)) if not var.get().strip() else None)
            self.widgets[lbl_txt] = w
        elif type == "spin":
            tk.Spinbox(self.inner, from_=range[0], to=range[1], textvariable=var, font=("Segoe UI", 10), bg=ENTRY_BG, fg=TEXT, buttonbackground=CARD_BG, relief="flat").grid(row=self.row, column=0, sticky="w", pady=(0, 10))
            var.set(range[0])
        elif type == "combo":
            c = ttk.Combobox(self.inner, textvariable=var, values=options, font=("Segoe UI", 10), state="readonly")
            c.grid(row=self.row, column=0, sticky="ew", pady=(0, 10))
            c.current(0)
        elif type == "radio":
            f = tk.Frame(self.inner, bg=CARD_BG); f.grid(row=self.row, column=0, sticky="w", pady=(0,10))
            var.set(options[0])
            for o in options: tk.Radiobutton(f, text=o, variable=var, value=o, bg=CARD_BG, fg=TEXT, selectcolor=ENTRY_BG).pack(side="left", padx=(0,10))
        self.row += 1
        return var

    def _on_book(self):
        v = {k: var.get().strip() for k, var in self.vars.items()}
        err = []
        if not v["Name"] or v["Name"] == "Enter full name": err.append("Name required")
        if not v["Phone"].isdigit() or len(v["Phone"]) != 10: err.append("Invalid 10-digit Phone")
        if not v["Age"].isdigit() or not (1 <= int(v["Age"]) <= 120): err.append("Invalid Age (1-120)")
        if err: return messagebox.showerror("Error", "\n".join(err))

        tid = "TKT-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        fare = {"AC Sleeper": 850, "Non-AC Sleeper": 550, "AC Seater": 650, "Non-AC Seater": 400, "Volvo Multi-Axle": 1200}.get(v["Bus"], 500)
        total = fare * int(v["Seats"])
        
        sep = "="*50
        print(f"\n{sep}\n   🎫 BUS TICKET BOOKING — CONFIRMATION\n{sep}")
        for k, val in v.items(): print(f"   {k:15}: {val}")
        print(f"   Ticket ID      : {tid}\n   Total Fare     : ₹{total}\n   Booked At      : {datetime.now().strftime('%d-%b-%Y %H:%M')}\n{sep}\n   ✅ Booking Successful!\n{sep}")
        
        messagebox.showinfo("Confirmed ✅", f"Ticket ID: {tid}\nRoute: {v['Route']}\nFare: ₹{total}")

    def _on_reset(self):
        for k, var in self.vars.items():
            if k == "Name": var.set("Enter full name"); self.widgets["Passenger Name"].config(fg=TEXT_DIM)
            elif k == "Phone": var.set("10-digit mobile number"); self.widgets["Phone Number"].config(fg=TEXT_DIM)
            elif k == "Gender": var.set("Male")
            elif k == "Seats": var.set("1")
            elif k == "Age": var.set("1")

if __name__ == "__main__":
    print("\n" + "="*50 + "\n   Bus Ticket Booking System - Online\n" + "="*50)
    root = tk.Tk(); BusTicketBookingApp(root); root.mainloop()
