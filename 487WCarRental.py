import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
from datetime import datetime

# Establish a connection with MySQL database
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chad0704",
    database="projectDB"
)

cursor = cnx.cursor()

# Pricing for different car types
car_prices = {
    'sedan': 50,
    'SUV': 60,
    'pickup': 70,
    'van': 80
}

# Add a reservation to the database
def add_reservation(name, car_type, start_date, end_date):
    charge = calculate_charge(car_type, start_date, end_date)
    query = "INSERT INTO Reservations (name, car_type, start_date, end_date, charge) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (name, car_type, start_date, end_date, charge))
    cnx.commit()

# Calculate the charge based on car type and number of days
def calculate_charge(car_type, start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    days = (end - start).days
    return days * car_prices[car_type]

# Fetch reservations by customer name
def search_reservation_by_name(name):
    cursor.execute("SELECT * FROM Reservations WHERE name = %s", (name,))
    return cursor.fetchone()

# Update reservation return date and charge
def update_reservation(reservation_id, new_end_date):
    cursor.execute("SELECT car_type, start_date FROM Reservations WHERE id = %s", (reservation_id,))
    car_type, start_date = cursor.fetchone()
    new_charge = calculate_charge(car_type, start_date, new_end_date)
    cursor.execute("UPDATE Reservations SET end_date = %s, charge = %s WHERE id = %s", (new_end_date, new_charge, reservation_id))
    cnx.commit()

# GUI Setup
class RentalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Car Rental System")
        self.geometry("400x300")

        self.frames = {}
        for F in (LoginFrame, CustomerFrame, AdminFrame):
            frame = F(self, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginFrame)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

# Login Frame
class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Select Role", font=('Helvetica', 16))
        label.pack(pady=10)

        customer_button = tk.Button(self, text="Customer", command=lambda: controller.show_frame(CustomerFrame))
        customer_button.pack()

        admin_button = tk.Button(self, text="Admin", command=lambda: controller.show_frame(AdminFrame))
        admin_button.pack()

# Customer Frame
class CustomerFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Name").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Car Type").pack()
        self.car_type_entry = tk.Entry(self)
        self.car_type_entry.pack()

        tk.Label(self, text="Start Date (YYYY-MM-DD)").pack()
        self.start_date_entry = tk.Entry(self)
        self.start_date_entry.pack()

        tk.Label(self, text="End Date (YYYY-MM-DD)").pack()
        self.end_date_entry = tk.Entry(self)
        self.end_date_entry.pack()

        submit_button = tk.Button(self, text="Submit Reservation", command=self.submit_reservation)
        submit_button.pack()

        search_button = tk.Button(self, text="Search Reservation", command=self.search_reservation)
        search_button.pack()

        back_button = tk.Button(self, text="Back to Login", command=lambda: controller.show_frame(LoginFrame))
        back_button.pack()

    def submit_reservation(self):
        name = self.name_entry.get()
        car_type = self.car_type_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        try:
            add_reservation(name, car_type, start_date, end_date)
            messagebox.showinfo("Success", "Reservation submitted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit reservation: {e}")

    def search_reservation(self):
        name = self.name_entry.get()
        reservation = search_reservation_by_name(name)

        if reservation:
            reservation_id = reservation[0]
            new_end_date = tk.simpledialog.askstring("Extend Reservation", "Enter new end date (YYYY-MM-DD):")
            update_reservation(reservation_id, new_end_date)
            messagebox.showinfo("Success", "Reservation updated successfully!")
        else:
            messagebox.showerror("Error", "Reservation not found")

# Admin Frame
class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Admin - All Reservations").pack()

        self.text = tk.Text(self)
        self.text.pack()

        refresh_button = tk.Button(self, text="Refresh", command=self.load_reservations)
        refresh_button.pack()

        back_button = tk.Button(self, text="Back to Login", command=lambda: controller.show_frame(LoginFrame))
        back_button.pack()

    def load_reservations(self):
        self.text.delete(1.0, tk.END)
        cursor.execute("SELECT * FROM Reservations")
        reservations = cursor.fetchall()
        for res in reservations:
            self.text.insert(tk.END, f"ID: {res[0]}, Name: {res[1]}, Car Type: {res[2]}, Start Date: {res[3]}, End Date: {res[4]}, Charge: ${res[5]}\n")

# Run the application
if __name__ == "__main__":
    app = RentalApp()
    app.mainloop()
