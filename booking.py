import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime, timedelta
import json

class iPadBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("iPad Booking System")
        
        # Data structure for bookings
        self.periods = ["Lesson 1", "Lesson 2", "Lesson 3", "Rest", "Lesson 4", 
                       "Lesson 5", "Lesson 6", "Lunch time", "Lesson 7", "Lesson 8",
                       "Reading Time", "ECA"]
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.bookings = {}
        
        # Create main layout
        self.create_calendar_widget()
        self.create_weekly_view()
        self.create_control_buttons()
        
        # Load existing bookings
        self.load_bookings()

    def create_calendar_widget(self):
        # Create calendar widget in top right
        self.cal_frame = ttk.Frame(self.root)
        self.cal_frame.grid(row=0, column=2, padx=10, pady=5, sticky="ne")
        
        current_date = datetime.now()
        cal = calendar.monthcalendar(current_date.year, current_date.month)
        
        # Calendar header
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            ttk.Label(self.cal_frame, text=day).grid(row=0, column=i)
            
        # Calendar days
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    ttk.Label(self.cal_frame, text=str(day)).grid(row=week_num+1, column=day_num)

    def create_weekly_view(self):
        # Create weekly view table
        self.weekly_frame = ttk.Frame(self.root)
        self.weekly_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
        
        # Add headers
        ttk.Label(self.weekly_frame, text="Time").grid(row=0, column=0)
        for i, day in enumerate(self.days):
            ttk.Label(self.weekly_frame, text=day).grid(row=0, column=i+1)
            
        # Add time slots
        for i, period in enumerate(self.periods):
            ttk.Label(self.weekly_frame, text=period).grid(row=i+1, column=0)
            for j in range(5):  # 5 days
                text_var = tk.StringVar()
                entry = ttk.Entry(self.weekly_frame, textvariable=text_var)
                entry.grid(row=i+1, column=j+1)
                self.bookings[(self.days[j], period)] = text_var

    def create_control_buttons(self):
        # Create control buttons at bottom
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Add Record", command=self.add_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Record", command=self.edit_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Record", command=self.delete_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to File", command=self.export_to_file).pack(side=tk.LEFT, padx=5)

    def add_record(self):
        # Create popup window for adding record
        popup = tk.Toplevel(self.root)
        popup.title("Add Record")
        
        ttk.Label(popup, text="Day:").grid(row=0, column=0)
        day_var = tk.StringVar()
        day_combo = ttk.Combobox(popup, textvariable=day_var, values=self.days)
        day_combo.grid(row=0, column=1)
        
        ttk.Label(popup, text="Period:").grid(row=1, column=0)
        period_var = tk.StringVar()
        period_combo = ttk.Combobox(popup, textvariable=period_var, values=self.periods)
        period_combo.grid(row=1, column=1)
        
        ttk.Label(popup, text="Booking:").grid(row=2, column=0)
        booking_entry = ttk.Entry(popup)
        booking_entry.grid(row=2, column=1)
        
        def save():
            self.bookings[(day_var.get(), period_var.get())].set(booking_entry.get())
            self.save_bookings()
            popup.destroy()
            
        ttk.Button(popup, text="Save", command=save).grid(row=3, column=0, columnspan=2)

    def edit_record(self):
        # Similar to add_record but pre-fills existing data
        self.add_record()

    def delete_record(self):
        # Create popup for deletion confirmation
        popup = tk.Toplevel(self.root)
        popup.title("Delete Record")
        
        ttk.Label(popup, text="Day:").grid(row=0, column=0)
        day_var = tk.StringVar()
        day_combo = ttk.Combobox(popup, textvariable=day_var, values=self.days)
        day_combo.grid(row=0, column=1)
        
        ttk.Label(popup, text="Period:").grid(row=1, column=0)
        period_var = tk.StringVar()
        period_combo = ttk.Combobox(popup, textvariable=period_var, values=self.periods)
        period_combo.grid(row=1, column=1)
        
        def delete():
            self.bookings[(day_var.get(), period_var.get())].set("")
            self.save_bookings()
            popup.destroy()
            
        ttk.Button(popup, text="Delete", command=delete).grid(row=2, column=0, columnspan=2)

    def export_to_file(self):
        with open("ipad_bookings.txt", "w") as f:
            f.write("iPad Booking Schedule\n\n")
            f.write("Time\t" + "\t".join(self.days) + "\n")
            for period in self.periods:
                row = [period]
                for day in self.days:
                    row.append(self.bookings[(day, period)].get())
                f.write("\t".join(row) + "\n")

    def save_bookings(self):
        data = {f"{day}-{period}": self.bookings[(day, period)].get()
                for day in self.days
                for period in self.periods}
        with open("bookings.json", "w") as f:
            json.dump(data, f)

    def load_bookings(self):
        try:
            with open("bookings.json", "r") as f:
                data = json.load(f)
                for key, value in data.items():
                    day, period = key.split("-")
                    self.bookings[(day, period)].set(value)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = iPadBookingSystem(root)
    root.mainloop()
